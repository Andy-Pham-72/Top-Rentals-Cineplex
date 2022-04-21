# import custom module
from customlib.config.configdirectory import config_directory
from customlib.custom_logger.customlogger import set_logger
from customlib.custom_selenium.init_chrome import init_chrome_browser
from customlib.custom_selenium.lastest_download import latest_download_file
from customlib.custom_cineplex.RetrieveRental import RetrieveRental
from customlib.custom_cineplex.save_rentals_to_csv import save_rentals_to_csv_file

# import selenium module
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

# import tmdbsimple module
import tmdbsimple as tmdb

# import some basic modules
import os
import time
import csv
from datetime import datetime

# initilize config variable
my_config = config_directory('cineplex.ini','directory')
blob_config = config_directory('blobstorage.ini','blob_storage')
tmdb_config = config_directory('tmdb.ini', 'key')

storage_name = blob_config["storage_name"]
storage_key = blob_config["key"]
container_name = blob_config["container_name"]
log_file_name = "cineplex_scraper"
inside_log_name = "cineplex_scraper"

# set logger
logger, log_dir, log_name = set_logger(log_file_name)
            
# download url
url = my_config['url']

# path to the chrome driver
chrome_path = my_config['chrome_path']

# in this case I don't need download path for the init_chrome_browser() method but I still put a directory anyway
download_path = "/mnt/container-data/"

# set chrome driver
driver = init_chrome_browser(download_path, chrome_path, url)

# set timeout
timeout = 5
try:
    # path to all the movie list
    xpath_movie_list = my_config['xpath_movie_list']
    # wait until all the list links visible
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
    print(f'{datetime.now()}    downloading #{i}: {link} .......')
    i += 1 
    try:
        # xpath string linked to "title", "year", "synopsis" data in the html
        xpath_title_1    = my_config['xpath_title_1']
        xpath_title_2    = my_config['xpath_title_2']
        xpath_year       = my_config['xpath_year']
        xpath_synopsis_1 = my_config['xpath_synopsis_1']
        xpath_synopsis_2 = my_config['xpath_synopsis_2']

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
        rentals.append(RetrieveRental(title, year, synopsis))
        
    except Exception as err:
        logger.error("An error message: {}".format(err))

# write csv file
try: 
    directory_1 = my_config['directory_save1'] + datetime.today().strftime('%Y-%m-%d')+ ".csv"
    logger.info("Successfully scrapped the top 36 rental movies")   
except Exception as err:
    logger.error("An error message: {}".format(err))

# save csv file to the directory
try:
    save_rentals_to_csv_file(rentals_list = rentals, file_name = directory_1)
    logger.info("Successfully saved cineplex data to DBFS storage")
except Exception as err:
    logger.error("An error message: {}".format(err))

# assign the csv to a variable
table_1 = spark.read.option("header","true").option("sep",",").csv(directory_1[5:-4]+".csv")

# assign api key of the imdb
tmdb.API_KEY = tmdb_config['key']
# set timeout
tmdb.REQUESTS_TIMEOUT = (2,5)

# find the imdb unique number from the top rental movie titles
imdb_number=[]
search = tmdb.Search()
for i in final_list:
    response = search.movie(query = i)
    id = search.results[0]['id']
    movie = tmdb.Movies(id).info()
    print("Searching for corresponding imdb id...")
    print(movie['imdb_id'])
    # add the movie name and imdb id into variable
    imdb_number.append([movie['imdb_id'], i])

# create a dataframe from imdb_number variable
column = ["imdb_id","title"]
table_2 = spark.createDataFrame(data=imdb_number,schema =column)

# join 2 dataframes
try:
    table_3 = table_1.join(table_2, ['title'], "inner")
    logger.info("Added 'imdb_id' column into dataframe")
except Exception as err:
    logger.warning("A warning message: {}".format(err))
    
# set up an account access key 
spark.conf.set(
    "fs.azure.account.key.%s.blob.core.windows.net"%(storage_name),
    storage_key)

# transfer csv file into parquet and save to azure blob storage
try:
    table_3.write.parquet("wasbs://{}@{}.blob.core.windows.net/top_cineplex_rental/{}.parquet".format(container_name, storage_name,directory_1[-27:-4])) # eg: directory_1[-27:-4] is 'rentals-list-2022-04-21'
    logger.info("Moved %s.parquet to azure 'top_cineplex_rental' blob"%(directory_1[-27:-4]))
except Exception as err:
    logger.warning("A warning message: {}".format(err))
    
# transfer log file to azure blob storage
dbutils.fs.cp('file:%s'%(log_dir), 'wasbs://%s@%s.blob.core.windows.net//log/%s'%(container_name, storage_name, log_name))