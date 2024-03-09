from src.config import Config
from src.notification import Notification
from src.service import Service


if __name__ == "__main__":
    config = Config()

    service = Service(config)
    service.login()
    result = service.process_photos()

    notification = Notification(config)
    notification.notify_discord(result)
