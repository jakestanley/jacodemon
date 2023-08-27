from lib.py.notifications import Notifications
import os
import subprocess
import logging
from lib.py.logs import GetLogManager

_CMD = '''
on run argv
  display notification (item 2 of argv) with title (item 1 of argv)
end run
'''

class MacNotifications(Notifications):
    def __init__(self):
        super().__init__()
        self._logger = GetLogManager().GetLogger(__name__)
        
    def notify(self, title, body):
        subprocess.call(['osascript', '-e', _CMD, title, body])
        self.logNotification(title, body)

if __name__ == "__main__":
    notifications = MacNotifications()
    notifications.notify("Recording saved", "/Users/jake/Movies/balls.mkv")
