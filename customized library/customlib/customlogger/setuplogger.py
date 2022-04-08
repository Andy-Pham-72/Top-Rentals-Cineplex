import logging
from logging.handlers import RotatingFileHandler


def setup_logger(log_name):
    """
    the method that creates log files
    
    :param log_name: string
                The name of the log file
    :return: logger

    """

    MAX_BYTES = 10000000 # Maximum size for a log file

    # create logger
    logger = logging.getLogger(__name__) 
    logger.setLevel(logging.INFO) # the level should be the lowest level set in handlers
    
    # create file handler which logs even record messages
    info_handler = RotatingFileHandler(log_name, maxBytes=MAX_BYTES)
    info_handler.setLevel(logging.INFO)

    # create console handler with a higher log level
    error_handler = logging.StreamHandler()
    error_handler.setLevel(logging.ERROR)

    # create formatter and add to the handlers
    log_format = logging.Formatter('[%(levelname)s] %(asctime)s - %(message)s')
    info_handler.setFormatter(log_format)
    error_handler.setFormatter(log_format)

    # add the handlers to the logger
    logger.addHandler(info_handler)
    logger.addHandler(error_handler)
    
    return logger

logger = setup_logger()