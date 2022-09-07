import logging


def logging_helper(logging_level: str, logging_message: str):
    if logging_level.lower() == "info":
        logging.basicConfig(level=logging.INFO)
        logging.info(logging_message)
    elif logging_level.lower() == "warning":
        logging.basicConfig(level=logging.WARNING)
        logging.warning(logging_message)
    elif logging_level.lower() == "error":
        logging.basicConfig(level=logging.ERROR)
        logging.error(logging_message)