from lib.py.logs import LogManager
import os
import time
import platform

class IO:

    def __init__(self, lman: LogManager) -> None:
        self._logger = lman.GetLogger(__name__)

    def _wait_for_file_unlock(self, file):
        self._logger.warn("Locking checks not implemented on this platform")

    def RenameFile(self, path, newpath):
        with open(path, "rb") as file:
            self._wait_for_file_unlock(file)
        os.rename(path, newpath)

    def RemoveFile(self, path):
        with open(path, "rb") as file:
            self._wait_for_file_unlock(file)
        os.remove(path)

def GetIo(lman) -> IO:
    system = platform.system()
    if system == "Darwin":
        from lib.py.platform.macos.io import MacIo
        return MacIo(lman)
    elif system == "Windows":
        from lib.py.platform.windows.io import WinIo
        return WinIo(lman)
    else:
        return IO(lman)