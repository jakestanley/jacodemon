from jacodemon.misc.io import IO
from jacodemon.logs import LogManager, GetLogManager

import os
import time

_MAX_ATTEMPTS = 20

class WinIo(IO):

    def __init__(self) -> None:
        super().__init__()
        self._logger = GetLogManager().GetLogger(__name__)

    def RenameFile(self, path, newpath):
        if path == None:
            self._logger.error("Attempted to rename blank path?")
            return
        self._logger.debug(f"Attempting to rename {path} to {newpath}")
        attempts = 0
        while attempts < _MAX_ATTEMPTS:
            try:
                if os.path.isfile(path):
                    os.rename(path, newpath)
                    self._logger.debug(f"Renamed file successfully after {attempts+1} attempts")
                else:
                    self._logger.debug(f"Replay file '{path}' does not exist?")
                    attempts += 1
                return
            except PermissionError:
                attempts += 1
                self._logger.debug(f"Got PermissionError when attempting to rename file on attempt {attempts}")
                time.sleep(0.2*attempts)
            except FileNotFoundError:
                attempts += 1
                self._logger.debug(f"Got FileNotFoundError when attempting to rename {path} on attempt {attempts}")
                if os.path.isfile(newpath):
                    self._logger.debug(f"Looks like the file has already moved to {newpath}")
                    return
                else:
                    # just in case OBS is still doing something with the file
                    time.sleep(0.2 * attempts)
                
        self._logger.error(f"Failed to rename file {path} to {newpath}")
        raise Exception()

    def RemoveFile(self, path):
        self._logger.debug(f"Attempting to remove {path}")
        attempts = 0
        while attempts < _MAX_ATTEMPTS:
            try:
                os.remove(path)
                return
            except PermissionError:
                attempts += 1
                self._logger.debug(f"Got PermissionError when attempting to remove file on attempt {attempts}")
                time.sleep(0.2*attempts)
                
        self._logger.error(f"Failed to remove file {path}")
        raise Exception()

