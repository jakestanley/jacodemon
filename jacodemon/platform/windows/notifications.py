import logging
from jacodemon.logs import GetLogManager
from jacodemon.notifications import Notifications
from win11toast import notify

class WinNotifications(Notifications):
    def __init__(self):
        super().__init__()
        self._logger = GetLogManager().GetLogger(__name__)

    def notify(self, title, body):
        notify(title, body)
        self.logNotification(title, body)
