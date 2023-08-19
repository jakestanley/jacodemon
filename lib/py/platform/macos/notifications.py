from lib.py.macros import Notifications
import os, subprocess

_CMD = '''
on run argv
  display notification (item 2 of argv) with title (item 1 of argv)
end run
'''

class MacNotifications(Notifications):
    def __init__(self):
        super().__init__()
        
    def notify(self, title, body):
        subprocess.call(['osascript', '-e', _CMD, title, body])
