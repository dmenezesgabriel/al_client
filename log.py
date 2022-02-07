import logging


def set_logger_config(
    name: str,
    log_level: str,
    handlers: list,
) -> logging.Logger:
    """
    Set logger configuration.
    """
    logger = logging.getLogger(name)
    logger.setLevel(log_level)
    for handler in handlers:
        logger.addHandler(handler)
    return logger


def setup_loggers():
    """
    Configure loggers.
    """

    default_log_format = (
        "[%(asctime)s] %(levelname)s [%(name)s.%(funcName)s:%(lineno)d]"
        " %(message)s"
    )
    log_level = logging.DEBUG
    formatter = logging.Formatter(default_log_format)
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    handlers = [stream_handler]
    set_logger_config("adventure_land", log_level, handlers)
    set_logger_config("socketio", log_level, handlers)
