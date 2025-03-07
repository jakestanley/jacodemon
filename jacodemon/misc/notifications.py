import logging

import platform

class Notifications:
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

        
def GetNotifications() -> Notifications:
    system = platform.system()
    if system == "Darwin":
        from jacodemon.platform.macos.notifications import MacNotifications
        return MacNotifications()
    else:
        from jacodemon.platform.windows.notifications import WinNotifications
        return WinNotifications()
