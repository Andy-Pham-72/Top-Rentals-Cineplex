# import custome module
from customlib.config.configdirectory import config_directory
from customlib.customlogger.customlogger import set_logger

# import selenium module
import pickle as pkl
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

import os
import time
import csv
from datetime import datetime

# initilize config variable
my_config = config_directory('cineplex.ini','directory')
blob_config = config_directory('blobstorage.ini','blob_storage')

storage_name = blob_config["storage_name"]
storage_key = blob_config["key"]
container_name = blob_config["container_name"]
log_file_name = "cineplex_scraper"
inside_log_name = "cineplex_scraper"

# set logger
logger, log_dir, log_name = set_logger(log_file_name)

# create class to store data
class Rental:
    '''
    Class Rental to store "title", "year", "synopsis" data
    '''
    def __init__(self, title, year, synopsis):
        self.title = title
        self.year = year
        self.synopsis = synopsis

def save_rentals_to_csv_file(rentals_list, file_name):
    """
    function to write csv "rentals" variable to csv file
    
    :param:
    
    """
    with open(file_name, 'w') as csvfile:
        fieldnames = ['title', 'year', 'synopsis']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        
        for rental in rentals_list:
            
            writer.writerow({'title' : rental.title, 'year' : int(rental.year), 'synopsis' : rental.synopsis })
            
# download url
url = my_config['url']

# path to the chrome driver
chrome_path = my_config['chrome_path']

# set proxy to prevent selenium detector
PROXY = "23.23.23.23:3128" # IP:PORT or HOST:PORT
capabilities = dict(DesiredCapabilities.CHROME)
capabilities['proxy'] = {'proxyType': 'MANUAL','httpProxy': '23.23.23.23:3128','ftpProxy': '23.23.23.23:3128',\
                         'sslProxy': '23.23.23.23:3128','noProxy': '','class': "org.openqa.selenium.Proxy",'autodetect': False}
chrome_options = Options()
chrome_options.add_argument("--disable-notifications")
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--verbose')
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--disable-software-rasterizer')
chrome_options.add_argument('--headless')

# set chrome driver
driver = webdriver.Chrome(service=Service(chrome_path), options =chrome_options)
driver.get(url)

# set timeout
timeout = 5
try:
    xpath_movie_list = "//*[@id='movie-collections-grid']/div[2]/div"
    WebDriverWait(driver, timeout).until(EC.visibility_of_element_located((By.XPATH, xpath_movie_list)))
except TimeoutException as err:
    print("Timed out waiting for page to load")
    logger.error("An error message: {}".format(err))

# get all the top rental links using list comprehension combined with selenium
class_link = "movie-pdp-link"
titles_links = [item.get_attribute("href") for item in WebDriverWait(driver, timeout). \
                   until(EC.presence_of_all_elements_located((By.CLASS_NAME, class_link)))]

# create empty list    
rentals = []
i = 1

# append data into the list
for link in titles_links:
    driver.get(link)
    print(f'downloading #{i}: {link} .......')
    i += 1 
    try:
        # xpath string linked to "title", "year", "synopsis" data in the html
        xpath_title_1    = "//*[@id='main-content']/div[3]/div[1]/div/div[3]/div/div[1]/h1/span"
        xpath_title_2    = "//*[@id='main-content']/div[3]/div[1]/div/div[3]/div/div[2]/h1/span"
        xpath_year       = "//*[@id='main-content']/div[3]/div[1]/div/div[3]/div/div[1]/div[2]/span"
        xpath_synopsis_1 = "//*[@id='main-content']/div[3]/div[1]/div/div[3]/div/div[5]/div/div/span[1]"
        xpath_synopsis_2 = "//*[@id='main-content']/div[3]/div[1]/div/div[3]/div/div[7]/div/div/span[1]"

        # retrieve data
        title = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, xpath_title_1))).text
        year  = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, xpath_year))).text
        synopsis = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, xpath_synopsis_1))).text 
       
        # slow down the execution
        time.sleep(5)

    except TimeoutException as err:
        # retrieve data due to different html setup
        title = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, xpath_title_2))).text
        synopsis = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, xpath_synopsis_2))).text 
        logger.warning("An info message: {}".format(err))
        
    except Exception as err:
        logger.error("An error message: {}".format(err))
        
    # append data to rentals list
    try:
        rentals.append(Rental(title, year, synopsis))
        
    except Exception as err:
        logger.error("An error message: {}".format(err))
    


# write csv file
try: 
    directory_1 = my_config['directory_1'] + datetime.today().strftime('%Y-%m-%d')+ ".csv"
    logger.info("Successfully scrapped the top 36 rental movies")   
except Exception as err:
    logger.error("An error message: {}".format(err))
    
try:
    save_rentals_to_csv_file(rentals_list = rentals, file_name = directory_1)
    logger.info("Successfully saved cineplex data to DBFS storage")
except Exception as err:
    logger.error("An error message: {}".format(err))

# set up an account access key 
spark.conf.set(
    "fs.azure.account.key.%s.blob.core.windows.net"%(storage_name),
    storage_key)

# transfer log file to azure blob storage
dbutils.fs.cp('file:%s'%(log_dir), 'wasbs://%s@%s.blob.core.windows.net//log/%s'%(container_name, storage_name, log_name))