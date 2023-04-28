import logging
import os


def configure_logging():
    root_logger = logging.getLogger()

    # If logger exists
    if root_logger.handlers:
        return

    log_level = os.getenv('APP_LOG_LEVEL', 'DEBUG')
    root_logger.setLevel(log_level)

    formatter = logging.Formatter(
        fmt="[%(asctime)s] - %(levelname)s - %(process)d - %(name)s:%(lineno)d: %(message)s",
        datefmt="%d.%m.%Y %H:%M:%S"
    )

    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(log_level)
    stream_handler.setFormatter(formatter)
    root_logger.addHandler(stream_handler)
