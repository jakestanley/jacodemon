from lib.py.io import IO
from lib.py.logs import LogManager

import os
import time

class WinIo(IO):

    def __init__(self, lman: LogManager) -> None:
        super().__init__(lman)
        self._logger = lman.GetLogger(__name__)

    def RenameFile(self, path, newpath):
        self._logger.debug(f"Attempting to rename {path} to {newpath}")
        attempts = 0
        while attempts < 10:
            try:
                os.rename(path, newpath)
                return
            except PermissionError:
                attempts += 1
                self._logger.debug(f"Got PermissionError when attempting to rename file on attempt {attempts}")
                time.sleep(0.2*attempts)
            except FileNotFoundError:
                attempts += 1
                self._logger.debug(f"Got FileNotFoundError when attempting to rename file on attempt {attempts}")
                time.sleep(0.2 * attempts)
                
        self._logger.error(f"Failed to rename file {path} to {newpath}")

    def RemoveFile(self, path):
        self._logger.debug(f"Attempting to remove {path}")
        attempts = 0
        while attempts < 10:
            try:
                os.remove(path)
                return
            except PermissionError:
                attempts += 1
                self._logger.debug(f"Got PermissionError when attempting to remove file on attempt {attempts}")
                time.sleep(0.2*attempts)
                
        self._logger.error(f"Failed to remove file {path}")

