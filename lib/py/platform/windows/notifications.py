import logging
from lib.py.logs import GetLogManager
from lib.py.notifications import Notifications
from win11toast import notify

class WinNotifications(Notifications):
    def __init__(self):
        super().__init__()
        self._logger = GetLogManager().GetLogger(__name__)

    def notify(self, title, body):
        notify(title, body)
        self.logNotification(title, body)
