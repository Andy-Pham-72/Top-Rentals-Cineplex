import logging
import time
import datetime


def set_logger(log_file_name):
    """
    This method creates logging for ongoing record of the application events.
    The log files will be saved into the directory "/tmp/log/" from the databrick File System
    then will be transfered to Azure Blob Storage as the final destination.py

    :param log_file_name: str
                    The name of the log file which will concatenate with current datetime. 
                        eg: cineplex_scraper2022-04-16-03-59-56.log
    :param inside_log_name: str
                    The name to specify inside the log file.
    :return logger:
    """

    file_date = datetime.datetime.fromtimestamp(time.time()).strftime("%Y-%m-%d-%H-%M-%S")
    p_dir = '/tmp/log/'
    p_filename = log_file_name + file_date + '.log'
    p_logfile = p_dir + p_filename

    # Create logger
    logger = logging.getLogger(log_file_name)
    logger.setLevel(logging.DEBUG)

    # Create file handler which logs event debug messages
    fh = logging.FileHandler(p_logfile)

    # Create console handler with a higher log level
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)

    # Create formatter and add it to the handlers
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(process)d - %(message)s')

    # Set formatter
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)

    # Clearing old frequent log information to ignore
    if (logger.hasHandlers()):
        logger.handlers.clear()

    # Add the handlers to the logger
    logger.addHandler(fh)
    logger.addHandler(ch)

    return logger, p_logfile, p_filename
