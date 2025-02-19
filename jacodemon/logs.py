import logging
import sys

from jacodemon.model.options import Options, GetOptions

_SINGLETON = None

class LogManager:

    def GetLogger(self, name) -> logging.Logger:
        logger = logging.getLogger(name)

        options: Options = GetOptions()

        # TODO make this more programmatic
        if "INFO" in options.stdout_log_level:
            handler = logging.StreamHandler()
            handler.setLevel(logging.INFO)
            logger.addHandler(handler)

        if "DEBUG" in options.stdout_log_level:
            handler = logging.StreamHandler()
            handler.setLevel(logging.DEBUG)
            logger.addHandler(handler)

        if "WARN" in options.stdout_log_level or "WARNING" in options.stdout_log_level:
            handler = logging.StreamHandler()
            handler.setLevel(logging.WARN)
            logger.addHandler(handler)

        return logger

def GetLogManager() -> LogManager:
    global _SINGLETON
    if _SINGLETON is None:
        logging.basicConfig(
            level=logging.DEBUG,
            format='%(asctime)s - [%(levelname)s] %(name)s: %(message)s',
            filename='app.log',
            filemode='a'
        )
        _SINGLETON = LogManager()
    return _SINGLETON
