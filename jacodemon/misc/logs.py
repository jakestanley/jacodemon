import logging

def InitialiseLoggingConfig(stdout_log_level):

    level = logging.getLevelName(stdout_log_level.upper())

    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG)  # Capture all log levels

    # Create a file handler that logs everything
    file_handler = logging.FileHandler("app.log")
    file_handler.setLevel(logging.DEBUG)  # Log everything to the file

    # Create a console handler that logs only INFO and above
    console_handler = logging.StreamHandler()
    console_handler.setLevel(level)

    # Define a log format
    formatter = logging.Formatter('%(asctime)s - [%(levelname)s] %(name)s: %(message)s')

    # Attach formatter to handlers
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    # Add handlers to the root logger
    root_logger.addHandler(file_handler)
    root_logger.addHandler(console_handler)
