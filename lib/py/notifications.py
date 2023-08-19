import platform

class Notifications:
    def __init(self):
        self._warn = False
        pass

    def notify(self, title, body):
        if not self._warn:
            print("Notifications are not supported on this platform. Printing to console...")
            self._warn = True
        print(f"""
              Title: {title}\n
              Body: {body}
              """)
        
def GetNotifications() -> Notifications:
    system = platform.system()
    if system == "Darwin":
        from lib.py.platform.macos.notifications import MacNotifications
        return MacNotifications()
    else:
        from lib.py.platform.windows.notifications import WinNotifications
        return WinNotifications()
