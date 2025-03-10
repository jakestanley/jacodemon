import logging
from jacodemon.service.notification_service import NotificationService
from win11toast import notify

class WinNotificationService(NotificationService):
    def __init__(self):
        super().__init__()
        self._logger = logging.getLogger(self.__class__.__name__)

    def notify(self, title, body):
        notify(title, body)
        self.logNotification(title, body)
