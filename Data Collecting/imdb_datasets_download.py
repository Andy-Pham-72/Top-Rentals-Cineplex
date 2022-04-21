# import custom module
from customlib.config.configdirectory import config_directory
from customlib.custom_logger.customlogger import set_logger
from customlib.custom_selenium.init_chrome import init_chrome_browser
from customlib.custom_selenium.lastest_download import latest_download_file

# import some basic modules
import os
import time
import csv
from datetime import datetime

# import selenium module
from selenium.webdriver.common.by import By

# unzip modules
import gzip
import shutil


# initilize config variable
my_config = config_directory('imdb.ini','directory')
blob_config = config_directory('blobstorage.ini','blob_storage')

# assign the config into variables
chrome_driver_path = my_config['chrome_path']
url = my_config['url']
download_dir = my_config['directory_0']
log_file_name= my_config['log_file_name']
storage_name = blob_config['storage_name']
container_name = blob_config['container_name']
storage_key =blob_config['key']

# set logger
logger, log_dir, log_name = set_logger(log_file_name)

# initialize a Chrome browser
driver = init_chrome_browser(download_dir, chrome_driver_path, url)

# list of files
download_list = ['title.akas.tsv.gz','title.basics.tsv.gz','title.crew.tsv.gz','title.principals.tsv.gz','title.ratings.tsv.gz','name.basics.tsv.gz']

# download raw files                 
for i in range(len(download_list)):
    try:
        driver.find_element(by=By.LINK_TEXT,value=download_list[i]).click()
        #driver.find_element(by=By.LINK_TEXT, value=download_list[i]).click()
        print(f'downloading: {download_list[i]}.......')
        logger.info("Found the download url #%s/%s."%(url,download_list[i]))
        
    except DeprecationWarning as err:
        logger.warning("A message: {}".format(err))
    except Exception as err:
        logger.error("An error message: {}".format(err))

# wait for all downloads to finish
file_ends = my_config['file_ends']

while "crdownload" == file_ends:
    time.sleep(1)
    try:
        newest_file = latest_download_file(path = download_dir)
        if "crdownload" in newest_file:
            file_ends = "crdownload"
        else:
            file_ends = "none"
    except Exception as err:
        print(err)

logger.info('Downloaded all files')

# set up an account access key 
spark.conf.set(
    "fs.azure.account.key.%s.blob.core.windows.net"%(storage_name),
    storage_key)

# move all the downloaded files to azure blob
dbutils.fs.cp('file:%s'%(download_dir), 'wasbs://%s@%s.blob.core.windows.net//raw_data/'%(container_name, storage_name), True)
logger.info('Moved all files to "raw_data" blob')

# unzip gz files
for i in range(len(download_list)):
    time.sleep(3)
    output_dir = "/dbfs/mnt/imdb/extracted/"
    with gzip.open( download_dir+"/"+ download_list[i] , 'rb') as f_in:
        with open( output_dir +"/"+ download_list[i][:-3] , 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)
logger.info('Unzipped all files to %s'%(output_dir))

# convert TSV files into parquet and save to azure blob storage
for i in download_list:
    table = spark.read.option("header","true").option("sep","\t").csv(output_dir[5:]+"/"+i[:-3] ) # output_dir[5:] is '/mnt/imdb/extracted/' and i[:-3] is the name of downloaded files eg: 'title.akas.tsv'
    table.write.parquet("wasbs://{}@{}.blob.core.windows.net/extracted_data/{}.parquet".format(container_name, storage_name,i[:-7]) )

logger.info('Moved all files to "extracted_data" blob')

# transfer log file to azure blob storage
dbutils.fs.cp('file:%s'%(blob_config['fs_log_dir']), 'wasbs://%s@%s.blob.core.windows.net//log/'%(container, storage_account), True)