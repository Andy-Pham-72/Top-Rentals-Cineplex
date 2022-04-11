import logging
import sys
from azure_storage_logging.handlers import BlobStorageRotatingFileHandler


def setup_logger(log_name, account_name, account_key, container_name):
    """
    the method that creates log files
    
    :param log_name: str
                The name of the log file. eg: "service.log"
    :param account_name: str
                The name of storage account
    :param account_key: str
                The key of storage account
    :param container_name: str
                The name of container

    :return: logger

    """

    logger = logging.getLogger('service_logger')
    log_formater = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(process)d - %(message)s')
    azure_blob_handler = BlobStorageRotatingFileHandler(filename = log_name, 
                                                            account_name= account_name,
                                                            account_key= account_key,
                                                            maxBytes=5,
                                                            container= container_name)
    azure_blob_handler.setLevel(logging.INFO)
    azure_blob_handler.setFormatter(log_formater)
    logger.addHandler(azure_blob_handler)

    logger.warning('warning message')
    
    return logger
