# iCloud Photos cleanup tool
This script will help you with cleaning up your iCloud disk space. 

Features:
- Delete all iCloud photos older than `X` days with `--min-days`. For example if you want to keep only 2 last months of photos in your library then you would write `--min-days 60`
- Keep only `X` amount of recent photos and delete the rest with `--min-amount`. For example if you want to keep only 1000 photos in your library then you would write `--min-amount 1000`
- Keep only `X` megabytes of recent photos and delete the rest with `--min-size`. For example if you want your photo library to take maximum 3GB then you would write `--min-size 3000`


Additionaly you can combine any of the above with the following:
- If you want to additionally to always delete too large photos then use `--max-photo-size`. This is especially good with `--min-size` because videos tend to take a lot of space so this way you can always delete the videos and keep in iCloud way more photos.

## Read first
- All interaction with iCloud is done through [pyicloud](https://github.com/picklepete/pyicloud) library. This script just loops over iCloud photos and deletes them if needed.
- This script does not download iCloud photos but it needs them in case you use safe mode with `--directory` param. For downloading simply use the [iCloud Photos Downloader](https://github.com/icloud-photos-downloader/icloud_photos_downloader) or [iCloud Photos Sync](https://github.com/steilerDev/icloud-photos-sync).
- If all you want is to download all your iCloud photos and then delete them then you might as well just use [iCloud Photos Downloader](https://github.com/icloud-photos-downloader/icloud_photos_downloader) with `--delete-after-download` option.
- The way iCloud works is that is syncs all photos between all your devices. This means that if you delete photos with this script then they will also be deleted from your phone. If you want to clean your iCloud without losing photos on your phone then the only way is to disable iCloud sync on your iPhone, delete photos on iCloud and then enable the sync on iPhone again.
- If you use 2FA (you should) then this script (or any other) will keep asking for your 2FA code that will last for some time. This means you cannot build a fully automated solution and you will have to enter this code from time to time. You have to disable 2FA to have an automated solution if you really need to.

## About iPhone photo backups
Initially I wanted to use iCloud as a backup tool for my iPhone photos on my Ubuntu based home server. Unfortunately there were 2 issues that made me to abandon this idea:
- With 2FA enabled you cannot have a fully automated setup (Configure and forget)
- Since Apple is stupid they made iCloud only a 2 way sync solution. This means that even that you just want to cleanup iCloud because its disk space is full you would also have to delete all photos on your phone even if on your phone have plenty of space.

Although both of above have some workarounds and this might be not that bad if I would for example backup photos rarely like only once per month or even more (sicne the workarounds require some manual steps).

The issue with using other apps than iCloud to backup is that Apple made it really hard to create an app that can do things periodically in background such as photos backup. Still it is possible to be done and I found only 2 apps that do this properly and it works as a fully automated solution:
- Use [PhotoSync](https://www.photosync-app.com/home) (paid) then setup an automation using iOS Shortcuts app to backup your photos every evening and such. This is what I am using and it works.
- Use [Immich](https://immich.app/). This app also is able to backup photos in background and is growing rapidly so check it out.