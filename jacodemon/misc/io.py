import logging
import os
import platform

class IO:

    def __init__(self) -> None:
        self._logger = logging.getLogger(self.__class__.__name__)

    def _wait_for_file_unlock(self, file):
        self._logger.warning("Locking checks not implemented on this platform")

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
        from jacodemon.platform.macos.io import MacIo
        return MacIo()
    elif system == "Windows":
        from jacodemon.platform.windows.io import WinIo
        return WinIo()
    else:
        return IO()