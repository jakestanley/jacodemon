import logging

class NotificationService:
    def __init(self):
        self._warn = False
        self._logger = logging.getLogger(self.__class__.__name__)

    def logNotification(self, title, body):
        self._logger.debug(f"Notification: {title} - {body}")

    def notify(self, title, body):
        if not self._warn:
            self._logger.warning("Notifications are not supported on this platform. Printing to console...")
            self._warn = True
        self.logNotification(title, body)
