import logging

log_format_stream = "[%(levelname)s] %(message)s"
log_format_file = "[%(levelname)s] %(funcName)2s:%(lineno)d - %(message)s"

file_handler = logging.FileHandler("app_sort.log")
file_handler.setLevel(logging.WARNING)
file_handler.setFormatter(logging.Formatter(log_format_file))

stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.INFO)
stream_handler.setFormatter(logging.Formatter(log_format_stream))


def get_logger(name, level):
    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(stream_handler)
    logger.addHandler(file_handler)

    return logger
