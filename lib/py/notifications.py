import logging
from lib.py.logs import LogManager
import platform

class Notifications:
    def __init(self, lman: LogManager):
        self._warn = False
        self._logger = lman.GetLogger(__name__)

    def logNotification(self, title, body):
        self._logger.debug(f"Notification: {title} - {body}")

    def notify(self, title, body):
        if not self._warn:
            self._logger.warning("Notifications are not supported on this platform. Printing to console...")
            self._warn = True
        self.logNotification(title, body)

        
def GetNotifications(lman: LogManager) -> Notifications:
    system = platform.system()
    if system == "Darwin":
        from lib.py.platform.macos.notifications import MacNotifications
        return MacNotifications(lman)
    else:
        from lib.py.platform.windows.notifications import WinNotifications
        return WinNotifications(lman)
