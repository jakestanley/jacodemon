import logging
from lib.py.options import Options

def configure():
    # log all messages to app.log
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s - [%(levelname)s] %(name)s: %(message)s',
        filename='app.log',
        filemode='a'
    )

class LogManager:
    def __init__(self, options: Options) -> None:
        self.options = options

    def GetLogger(self, name) -> logging.Logger:
        logger = logging.getLogger(name)

        # TODO make this more programmatic
        if "INFO" in self.options.stdout_log_level:
            handler = logging.StreamHandler()
            handler.setLevel(logging.INFO)
            logger.addHandler(handler)

        if "DEBUG" in self.options.stdout_log_level:
            handler = logging.StreamHandler()
            handler.setLevel(logging.DEBUG)
            logger.addHandler(handler)

        if "WARN" in self.options.stdout_log_level or "WARNING" in self.options.stdout_log_level:
            handler = logging.StreamHandler()
            handler.setLevel(logging.WARN)
            logger.addHandler(handler)

        return logger

