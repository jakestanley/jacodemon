from jacodemon.notifications import Notifications
import subprocess
import logging

_CMD = '''
on run argv
  display notification (item 2 of argv) with title (item 1 of argv)
end run
'''

class MacNotifications(Notifications):
    def __init__(self):
        super().__init__()
        self._logger = logging.getLogger(self.__class__.__name__)
        
    def notify(self, title, body):
        subprocess.call(['osascript', '-e', _CMD, title, body])
        self.logNotification(title, body)

if __name__ == "__main__":
    notifications = MacNotifications()
    notifications.notify("Recording saved", "/Users/jake/Movies/balls.mkv")
