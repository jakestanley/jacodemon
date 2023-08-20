from lib.py.io import IO

import os
import time

class WinIo(IO):

    def __init__(self) -> None:
        super().__init__()

    def RenameFile(self, path, newpath):
        attempts = 0
        while attempts < 10:
            try:
                os.rename(path, newpath)
                return
            except PermissionError:
                attempts += 1
                time.sleep(0.2*attempts)
                
        print("Failed to rename file")

    def RemoveFile(self, path):
        attempts = 0
        while attempts < 10:
            try:
                os.remove(path)
                return
            except PermissionError:
                attempts += 1
                time.sleep(0.2*attempts)
                
        print("Failed to remove file")

