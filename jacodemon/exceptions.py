class ObsControllerException(Exception):
    def __init__(self, cause: Exception):
        super().__init__()
        self.cause = cause