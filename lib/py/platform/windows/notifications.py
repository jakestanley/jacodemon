import logging
from lib.py.logs import LogManager
from lib.py.notifications import Notifications
from win11toast import toast, notify

class WinNotifications(Notifications):
    def __init__(self, lman: LogManager):
        super().__init__()
        self._logger = lman.GetLogger(__name__)

    def notify(self, title, body):
        notify(title, body)
        self.logNotification(title, body)
