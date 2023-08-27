import logging
from lib.py.logs import GetLogManager
import platform

class Notifications:
    def __init(self):
        self._warn = False
        self._logger = GetLogManager().GetLogger(__name__)

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
        from lib.py.platform.macos.notifications import MacNotifications
        return MacNotifications()
    else:
        from lib.py.platform.windows.notifications import WinNotifications
        return WinNotifications()
