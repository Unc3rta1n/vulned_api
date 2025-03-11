import logging


class CustomFormatter(logging.Formatter):
    grey = "\x1b[38;20m"
    green = "\x1b[32m"
    yellow = "\x1b[33;20m"
    red = "\x1b[31;20m"
    bold_red = "\x1b[31;1m"
    reset = "\x1b[0m"
    format = "[%(name)s] [%(asctime)s] %(levelname)s - [%(filename)s:%(funcName)s:%(lineno)d] %(message)s"

    FORMATS = {
        logging.DEBUG: grey + format + reset,
        logging.INFO: green + format + reset,
        logging.WARNING: yellow + format + reset,
        logging.ERROR: red + format + reset,
        logging.CRITICAL: bold_red + format + reset,
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt, datefmt="%d.%m.%y-%H:%M:%S")
        return formatter.format(record)


def setup_logger(name: str, level: str) -> logging.Logger:

    formatter = CustomFormatter()
    logger = logging.getLogger(name)
    logger.setLevel(level)

    logger.handlers = []

    handler = logging.StreamHandler()
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    return logger

logger = setup_logger("fastapi_app", logging.INFO)