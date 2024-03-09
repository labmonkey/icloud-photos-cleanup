from src.config import Config
from tzlocal import get_localzone
from src.photo import Photo
from pyicloud import PyiCloudService
import sys
import os
import datetime

class Service:

    config: Config
    api: PyiCloudService

    def __init__(self, config):
        self.config = config

    def login(self):
        self.api = PyiCloudService(self.config.args.username, self.config.args.password)

        if self.api.requires_2fa:
            print("Two-factor authentication required.")
            code = input(
                "Enter the code you received of one of your approved devices: "
            )
            result = self.api.validate_2fa_code(code)
            print("Code validation result: %s" % result)

            if not result:
                print("Failed to verify security code")
                sys.exit(1)

            if not self.api.is_trusted_session:
                print("Session is not trusted. Requesting trust...")
                result = self.api.trust_session()
                print("Session trust result %s" % result)

                if not result:
                    print(
                        "Failed to request trust. You will likely be prompted for the code again in the coming weeks"
                    )

    def process_photos(self):
        # Loop through all photos in the 'All Photos' album
        photos = self.api.photos.all
        photos.direction = "ASCENDING" # recent first

        result = Result()
        result.total_photos_before = len(photos)

        print(f"[iCloud] Total photos to process: {result.total_photos_before}")

        photosIndex = 0
        totalPhotosCounter = 0
        totalPhotosSizeCounter = 0
        photoThresholdReached = False

        for photo_raw in photos:
            photosIndex += 1
            photo = Photo(photo_raw, photosIndex)

            print(
                f"[iCloud] [#{photo.index}] Processing: {photo.photo.filename} : {'{:%Y-%m-%d}'.format(photo.photo.created.astimezone(get_localzone()))}"
            )

            photo_size_bytes = photo.get_photo_size_bytes()

            totalPhotosCounter += 1
            totalPhotosSizeCounter += photo_size_bytes
            if not photoThresholdReached and self.should_keep_photo(
                photo.photo.added_date, totalPhotosCounter, totalPhotosSizeCounter
            ):
                print(f"[iCloud] [#{photo.index}] Keeping photo")
                continue
            else:
                photoThresholdReached = True

            if self.delete_photo(photo):
                result.total_photos_deleted += 1
            else:
                result.total_errors += 1

        print(f"[iCloud] Total photos size: '{totalPhotosSizeCounter/1024/1024} MB'")

        result.total_photos_after = result.total_photos_before - result.total_photos_deleted

        return result

    def should_keep_photo(self, photo: Photo, totalPhotosCounter, totalPhotosSizeCounter):
        if self.config.args.min_amount and totalPhotosCounter < self.config.args.min_amount:
            return True
        if (
            self.config.args.min_size
            and totalPhotosSizeCounter / 1024 / 1024 < self.config.args.min_size
        ):
            return True
        if self.config.args.min_days:
            delta = photo.photo.added_date - self.config.today
            return not (delta.days > self.config.args.min_days)
        
        photo_size_megabytes = photo.get_photo_size_megabytes()
        if photo_size_megabytes > int(self.config.args.max_photo_size):
            print(
                f"[iCloud] [#{photo.index}] The photo has '{photo_size_megabytes} MB' which is above given max size"
            )
            return False

        return False

    def delete_photo(self, photo: Photo):
        print(f"[iCloud] [#{photo.index}] Deleting photo")
        canDelete = True
        try:
            if self.config.args.directory:
                print(
                    f"[iCloud] [#{photo.index}] Safe mode is enabled. Checking if there is local copy of file first."
                )
                dir = os.path.abspath(self.config.args.directory)
                # directory format is the default one from icloud-photo-backup project
                subpath = "{:%Y/%m/%d}".format(
                    photo.photo.created.astimezone(get_localzone())
                )
                path = f"{dir}/{subpath}/{photo.photo.filename}"
                pathExists = os.path.exists(path)
                existsString = "Exists" if pathExists else "Not Exists"
                print(f"[iCloud] [#{photo.index}] File '{path}' : {existsString}")
                if not pathExists:
                    canDelete = False

            if canDelete:
                photo.photo.delete()
                print(f"[iCloud] [#{photo.index}] Deleted photo: {photo.photo.filename}")
                return True
            else:
                print(
                    f"[iCloud] [#{photo.index}] Did not delete photo: {photo.photo.filename}"
                )
                return False

        except Exception as e:
            print(
                f"[iCloud] [#{photo.index}] Failed to delete photo: {photo.photo.filename}. Error: {e}"
            )
            return False


class Result:
    total_photos_before: int = 0
    total_photos_after: int = 0
    total_photos_deleted: int = 0
    total_errors: int = 0
