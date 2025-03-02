import logging
from jacodemon.notifications import Notifications
from win11toast import notify

class WinNotifications(Notifications):
    def __init__(self):
        super().__init__()
        self._logger = logging.getLogger(self.__class__.__name__)

    def notify(self, title, body):
        notify(title, body)
        self.logNotification(title, body)
