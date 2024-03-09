import requests
from src.service import Result


class Notification:

    def __init__(self, config):
        self.config = config

    def notify_discord(self, data: Result):
        if not self.config.args.discord_webhook:
            return
        
        message = {
            "username": "iCloud Photos cleanup tool",
            "embeds": [
                {
                    "description": "Summary of the recent cleanup job",
                    "fields": [
                        {
                            "name": "Total Photos Before",
                            "value": data.total_photos_before,
                        },
                        {
                            "name": "Total Photos After",
                            "value": data.total_photos_after,
                        },
                        {"name": "Deleted Photos", "value": data.total_photos_deleted},
                        {"name": "Errors", "value": data.total_errors},
                    ],
                }
            ],
        }

        # Send the notification
        response = requests.post(
            self.config.discord_webhook,
            json=message,
            headers={"Content-Type": "application/json"},
        )

        # Check the response status code
        if response.status_code == 204:
            print("[Notification] Discord notification sent successfully.")
        else:
            print(
                "[Notification] Error sending Discord notification:",
                response.status_code,
                response.reason,
            )
