import logging


def get_logger(name: str, level: int = logging.DEBUG) -> logging.Logger:
    logger = logging.getLogger(name)
    if not logger.handlers:
        logger.addHandler(get_sys_out_handler())
    logger.setLevel(level)
    return logger


def get_default_formatter() -> logging.Formatter:
    return logging.Formatter(
        "%(asctime)s - %(funcName)s - %(levelno)s - %(levelname)s - %(message)s"
    )


def get_sys_out_handler() -> logging.Handler:
    handler = logging.StreamHandler()
    handler.setFormatter(get_default_formatter())
    return handler


def clear_handlers(logger: logging.Logger) -> logging.Logger:
    for handler in logger.handlers[:]:
        handler.flush()
        handler.close()
        logger.removeHandler(handler)
    return logger
