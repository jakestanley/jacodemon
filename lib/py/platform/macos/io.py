import fcntl

from lib.py.io import IO

class MacIo(IO):

    def __init__(self, lman) -> None:
        super().__init__(lman)
        self._logger = lman.GetLogger(__name__)

    def _wait_for_file_unlock(self, file):
        try:
            fcntl.flock(file, fcntl.LOCK_EX)  # Acquire an exclusive lock
        except BlockingIOError:
            # The file is currently locked; wait until it's unlocked
            fcntl.flock(file, fcntl.LOCK_EX)  # Wait until the lock is acquired
        finally:
            fcntl.flock(file, fcntl.LOCK_UN)  # Release the lock
