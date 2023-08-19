from lib.py.notifications import Notifications
from win10toast import ToastNotifier

class WinNotifications(Notifications):
    def __init__(self):
        super().__init__()
        self.toast = ToastNotifier()

    def notify(self, title, body):
        self.toast.show_toast(title, body, duration = 20, icon_path = "icon.ico", threaded = True)
