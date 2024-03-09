from pyicloud.services.photos import PhotoAsset

class Photo:

    photo: PhotoAsset
    index: int

    def __init__(self, photo: PhotoAsset, index):
        self.photo = photo
        self.index = index

    def get_photo_size_bytes(self):
        photoSize = 0
        # No idea how iCloud treats the photo size. Is it only original size or all versions? I assume all of them.
        for resolution, values in self.photo.versions.items():
            photoSize += int(values["size"])
        return photoSize
        # return photo.size; # alternative

    def get_photo_size_megabytes(self):
        # No idea if iCloud counts 1kb = 1000 or 1024 bytes. I assume the "proper" one
        return self.get_photo_size_bytes(self.photo) / 1024 / 1024
