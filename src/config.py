import argparse
import datetime
from tzlocal import get_localzone

class Config:

    today: datetime

    def __init__(self):
        self.parse_arguments()
        self.today = datetime.datetime.now()
        self.print_summary()

    def parse_arguments(self):
        parser = argparse.ArgumentParser(
            description="Process iCloud photo management script arguments."
        )

        parser.add_argument(
            "-e",
            "--username",
            type=str,
            required=True,
            help="The email address to use for iCloud photo management",
        )
        parser.add_argument(
            "-p",
            "--password",
            type=str,
            required=True,
            help="The password to use for iCloud photo management",
        )
        parser.add_argument(
            "-a",
            "--min-amount",
            type=int,
            help="The minimum amount of photos",
        )
        parser.add_argument(
            "-s",
            "--min-size",
            type=int,
            help="The maximum size of photos to process in megabytes (default: 4000 MB)",
        )
        parser.add_argument(
            "-d",
            "--min-days",
            type=int,
            help="The date to filter photos (format: dd-mm-yyyy)",
        )
        parser.add_argument(
            "-dir",
            "--directory",
            type=str,
            help="The directory with iCloud backup photos",
        )
        parser.add_argument(
            "-ms",
            "--max-photo-size",
            type=int,
            help="Always delete photos above given size in MB",
        )
        parser.add_argument(
            "-ds",
            "--discord-webhook",
            type=int,
            help="Full webhook link to your discord channel for notifications",
        )

        self.args = parser.parse_args()

    def print_summary(self):
        print("[Config] Initialized script with following configuration:")
        if self.args.min_amount:
            print(f"[Config] - Keep at least '{self.args.min_amount}' photos")
        if self.args.min_size:
            print(f"[Config] - Keep at least '{self.args.min_size} MB' of photos")
        if self.args.min_days:
            print(f"[Config] - Keep at least '{self.args.min_days}' days of photos")
        if self.args.max_photo_size:
            print(f"[Config] - Always delete photos above '{self.args.max_photo_size} MB'")
        if self.args.directory:
            print(f"[Config] - Delete photos only if they exist in '{self.args.directory}' (\":%Y/%m/%d\" structure)")
        print("[Config] Note that if you provided multiple conditions then the photos will be deleted starting from the first condition that is met.")