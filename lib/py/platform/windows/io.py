from lib.py.io import IO

import msvcrt
import time

class WinIo(IO):

    def __init__(self) -> None:
        super().__init__()

    def _wait_for_file_unlock(self, file):
        super()._wait_for_file_unlock(file)
        # TODO: below code does not work so use parent for now
        # while True:
        #     try:
        #         msvcrt.locking(file.fileno(), msvcrt.LK_NBLCK, 1)
        #         break
        #     except IOError:
        #         time.sleep(0.1)  # Wait and try again
