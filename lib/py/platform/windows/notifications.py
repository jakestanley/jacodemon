from lib.py.notifications import Notifications
from win11toast import toast

class WinNotifications(Notifications):
    def __init__(self):
        super().__init__()

    def notify(self, title, body):
        toast(title, body)
