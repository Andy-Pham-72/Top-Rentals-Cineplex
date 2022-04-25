# import custom module
from customlib.config.configdirectory import config_directory
from customlib.custom_logger.customlogger import set_logger
from customlib.custom_selenium.init_chrome import init_chrome_browser

# import selenium module
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# import tmbd and rottentomatoes modules to retrieve movie data
from rotten_tomatoes_scraper.rt_scraper import MovieScraper

# import pyspark modules
from pyspark.sql.functions import row_number, monotonically_increasing_id
from pyspark.sql import Window


# import some basic modules
import time
from datetime import datetime



# initilize config variable
my_config = config_directory('cineplex.ini','directory') # to get the chrome_path and directory of the top rental file
blob_config = config_directory('blobstorage.ini','blob_storage')
tmdb_config = config_directory('tmdb.ini', 'key')
rotten_config = config_directory('rotten_review.ini', 'review')

storage_name = blob_config["storage_name"]
storage_key = blob_config["key"]
container_name = blob_config["container_name"]
directory_1 = my_config['directory_save1']
file_name = rotten_config['file_name']

log_file_name = "critics_review"

# set logger
logger, log_dir, log_name = set_logger(log_file_name)

# path to the chrome driver
chrome_path = my_config['chrome_path']

# in this case I don't need download path for the init_chrome_browser() method but I still put a directory anyway
download_path = "/mnt/container-data/"

# set up an account access key 
spark.conf.set(
    "fs.azure.account.key.%s.blob.core.windows.net"%(storage_name),
    storage_key)

# get the today top cineplex rental data
directory_1 = directory_1 + datetime.today().strftime('%Y-%m-%d')

# assign the file data into a variable
df = spark.read.option("header","true").parquet("wasbs://{}@{}.blob.core.windows.net/top_cineplex_rental/{}.parquet".format(container_name, storage_name,directory_1[-23:]))

# query all the movie titles from the top rental movie dataframe
title = df.select('title').toPandas()['title']

# create a list
critics = []

# create variables to grab the elements of the url
row_class = rotten_config['row_class']
review_class = rotten_config['review_class']
name_class = rotten_config['name_class']
alternate_class = rotten_config['alternate_class']
top_critics_end_link = rotten_config['top_critics_end_link']
search_url = rotten_config['search_url']

# for loop to retrieve the dataset of top critics review from rotten tomatoes
for i in title:
    # search movie info by the title
    try:
        movie_scraper = MovieScraper(movie_title=i.lower())
        # assign imdb id for the corresponding movie title
        imdb_id = a.select(a.imdb_id).filter(a.title == i).collect()[0][0]
        # slower the script
        time.sleep(1)
        # logger
        logger.info("Getting the imdb unique id: {}".format(imdb_id))
        
    except Exception as err:
        logger.warning("A warning message: {}".format(err))
        
    try:
        # get the rotten tomatoes movie link
        movie_scraper.extract_metadata()
        # combine the string for the top critics url
        url = movie_scraper.url + top_critics_end_link
        # logger
        logger.info("Getting the rotten tomatoes top critic url: {}".format(url))
        # initialize the chrome browser
        driver = init_chrome_browser(download_path, chrome_path, url)
        
    except Exception as err:
        logger.warning("A warning message: {}".format(err))
        
        # create a search link for the alternate url due to timeout issue from the code above
        link = search_url+i.split()[0]
        
        for n in range(len(i.split()[1:])):
            print(i.split()[n])
            link= link + "%20" +i.split()[1:][n] # combine the components of the search link by adding "%20" eg: "https://www.rottentomatoes.com/search?search=the%20batman"
            # logger
        logger.info("Getting the search rotten tomatoes url for the alternate critic url: {}".format(link))
        # initialize the chrome browser
        driver_1 = init_chrome_browser(download_path, chrome_path, link)
        # get the alternate url
        url = WebDriverWait(driver_1, 10).until(EC.visibility_of_element_located((By.XPATH, alternate_class))).get_attribute("href")
        # combine the string for the top critics url
        url = url + top_critics_end_link
        logger.info("Getting the alternate critic url: {}".format(url))
        # initialize the chrome browser
        driver = init_chrome_browser(download_path, chrome_path, url)
    
    # get all the critics review elements in the url
    rows = driver.find_elements(by=By.XPATH, value= row_class)
    
    # retrieve all the top critic reviews from the url
    for row in rows:
        print("downloading review...")
        critics_review = row.find_element(by=By.XPATH, value= review_class).text
        critics_name = row.find_element(by=By.XPATH, value= name_class).text
        # append the data into the list
        critics.append((imdb_id,critics_name,critics_review))
        

columns = ['imdb_id', 'reviewer', 'review']
table = spark.createDataFrame(data=critics,schema =columns)
table = table.withColumn("index", row_number().over(Window.orderBy(monotonically_increasing_id()))-1)
logger.info("Finished retrieving all the top critic review from the top rental movie list")

try:
    file_name = file_name + datetime.today().strftime('%Y-%m-%d')
    table.write.parquet("wasbs://{}@{}.blob.core.windows.net/top_rotten_tomatoes_critics/{}.parquet".format(container_name, storage_name,file_name))
    logger.info("Saved %s.parquet to azure 'top_rotten_tomatoes_critics' blob"%(file_name))
except Exception as err:
    logger.warning("A warning message: {}".format(err))

# transfer log file to azure blob storage
dbutils.fs.cp('file:%s'%(log_dir), 'wasbs://%s@%s.blob.core.windows.net//log/%s'%(container_name, storage_name, log_name))