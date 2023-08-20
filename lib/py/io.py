import os
import time
import platform

class IO:

    def __init__(self) -> None:
        pass

    def _wait_for_file_unlock(self, file):
        print("Locking checks not implemented on this platform")

    def RenameFile(self, path, newpath):
        with open(path, "rb") as file:
            self._wait_for_file_unlock(file)
        os.rename(path, newpath)

    def RemoveFile(self, path):
        with open(path, "rb") as file:
            self._wait_for_file_unlock(file)
        os.remove(path)

def GetIo() -> IO:
    system = platform.system()
    if system == "Darwin":
        from lib.py.platform.macos.io import MacIo
        return MacIo()
    elif system == "Windows":
        from lib.py.platform.windows.io import WinIo
        return WinIo()
    else:
        return IO()