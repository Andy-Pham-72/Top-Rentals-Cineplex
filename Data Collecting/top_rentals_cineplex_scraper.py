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

# import pyspark modules
from pyspark.sql.functions import row_number, monotonically_increasing_id, udf, lit, when, date_sub
from pyspark.sql import Window

# BlobClient
from azure.storage.blob import BlobClient

# import tmdbsimple module
import tmdbsimple as tmdb

# import some basic modules
import os
import time
import csv
from datetime import datetime,timedelta

# initilize config variable
my_config = config_directory('cineplex.ini','directory')
tmdb_config = config_directory('tmdb.ini', 'key')
blob_config = config_directory('blobstorage.ini','blob_storage')

# assign config string into variables
storage_name = blob_config["storage_name"]
storage_key = blob_config["key"]
conn_str = blob_config["conn_str"]
container_name = blob_config["container_name"]
log_file_name = "cineplex_scraper"
inside_log_name = "cineplex_scraper"

# set logger
logger, log_dir, log_name = set_logger(log_file_name)
            
# download url
url = my_config['url']

# path to the chrome driver
chrome_driver_path = my_config['chrome_path']

# in this case I don't need download path for the init_chrome_browser() method but I still put a directory anyway
download_path = "/mnt/container-data/"

# set chrome driver
driver = init_chrome_browser(download_path, chrome_driver_path, url)

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
        #xpath_synopsis_1 = my_config['xpath_synopsis_1']
        #xpath_synopsis_2 = my_config['xpath_synopsis_2']

        # retrieve data
        title = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, xpath_title_1))).text
        year  = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, xpath_year))).text
        #synopsis = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, xpath_synopsis_1))).text 
       
        # slow down the execution
        time.sleep(5)

    except TimeoutException as err:
        # retrieve data due to different html setup
        title = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, xpath_title_2))).text
        #synopsis = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, xpath_synopsis_2))).text 
        logger.warning("An info message: {}".format(err))
        
    except Exception as err:
        logger.error("An error message: {}".format(err))
        
    # append data to rentals list
    try:
        rentals.append(RetrieveRental(title, year))
        
    except Exception as err:
        logger.error("An error message: {}".format(err))

# quit driver
driver.quit()

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
title_source = spark.read.option("header","true").option("sep",",").csv(directory_1[5:-4]+".csv")

# assign api key of the imdb
tmdb.API_KEY = tmdb_config['key']
# set timeout
tmdb.REQUESTS_TIMEOUT = (2,5)

# create a list for the top rental movie titles and imdb_id
imdb_number = []

# initialize search engine
search = tmdb.Search()

# convert to get the top rental title list
final_list = title_source.select('title').toPandas()

# ordering variable
order_num = 0

# for loop to add data into top rental titles
for i in final_list['title']:
    # search by movie name
    response = search.movie(query = i)
    # assign the movie id
    id = search.results[0]['id']
    # assign info variable to look for "imdb_id"
    movie = tmdb.Movies(id).info()
    print("Searching for corresponding imdb id...")
    print(movie['imdb_id'])
    # ordering of the movies
    order_num += 1
    # add the movie name and imdb id into variable
    if movie['imdb_id'] == None:
        imdb_number.append([str(movie['id']), i, order_num]) # add the movie "database id" instead of "imdb_id" so we can for later update easily
    else:
        imdb_number.append([movie['imdb_id'], i, order_num])


# check if the top_synopsis.parquet file exists in the blob storage
blob = BlobClient.from_connection_string(conn_str=conn_str, container_name="capstone", blob_name="top_synopsis/top_synopsis.parquet")

# create a list for the top synopsis movie rentals
top_synopsis = []

if blob.exists() == True:
    # assign top_synopsis.parquet into df
    df = spark.read.parquet("wasbs://{}@{}.blob.core.windows.net/top_synopsis/top_synopsis.parquet".format(container_name, storage_name))
    # for loop to add data into top_synopsis table
    for i in final_list['title']:
        # search by movie name
        response = search.movie(query = i)
        # assign the movie id
        id = search.results[0]['id']
        # assign info variable to look for "imdb_id"
        movie = tmdb.Movies(id).info()
        print("Searching for corresponding imdb id...")
        print(movie['imdb_id'])
        # assign the imdb_id from synopsis_table into a variable
        list_id = synopsis_table.select('imdb_id').toPandas()['imdb_id']
        if movie['imdb_id'] == None and movie['id'] not in list_id:
            top_synopsis.append([str(movie['id']), movie['overview']])
        elif movie['imdb_id'] not in list_id:
            top_synopsis.append([movie['imdb_id'], movie['overview']])
        else:
            pass
else:
    # for loop to add data into top_synopsis table
    for i in final_list['title']:
        # search by movie name
        response = search.movie(query = i)
        # assign the movie id
        id = search.results[0]['id']
        # assign info variable to look for "imdb_id"
        movie = tmdb.Movies(id).info()
        print("Searching for corresponding imdb id...")
        print(movie['imdb_id'])
        if movie['imdb_id'] == None :
            top_synopsis.append([str(movie['id']), movie['overview']])
        else:
            top_synopsis.append([movie['imdb_id'], movie['overview']])

# create 2 dataframes from imdb_number variable
# columns for the top synopsis
column_1 = ["imdb_id", "synopsis"]
synopsis_table = spark.createDataFrame(data=top_synopsis,schema =column_1)
# adding surrogate key
synopsis_table = synopsis_table.withColumn('synopsis_id', row_number().over(Window.orderBy(monotonically_increasing_id())))
try:
    table_source.write.parquet("wasbs://{}@{}.blob.core.windows.net/top_synopsis/top_synopsis.parquet".format(container_name, storage_name)) 
    logger.info("Moved top_synopsis.parquet to azure 'top_synopsis' blob")
except Exception as err:
    logger.warning("A warning message: {}".format(err))

# columns for the top rental 
column_2 = ["src_imdb_id","src_title", "ordering"]
table_source = spark.createDataFrame(data=imdb_number,schema =column_2)

# set up an account access key 
spark.conf.set(
                "fs.azure.account.key.%s.blob.core.windows.net"%(storage_name),
                storage_key )

# variable for end_date later on
high_date = datetime.strptime('9999-12-31', '%Y-%m-%d').date()
print(high_date)
# variable for current_date later on
current_date = datetime.today().date()
print(current_date)

# assign historical day so we can find the corresponding parquet file
days = timedelta(7)
history = datetime.today().date() - days


# check if the target file exists in the blob storage
blob = BlobClient.from_connection_string(conn_str=conn_str, container_name="capstone", blob_name="top_cineplex_rental/rentals-list-{}.parquet".format(history))

# assign dictionary for the column names in order
column_names = ['imdb_id', 'title', 'ordering', 'is_current', 'start_date', 'end_date']

if blob.exists() == True:

    # prepare for merge - added effective and end date
    table_source_new = table_source.withColumn('src_start_date', lit(current_date)).withColumn('src_end_date', lit(high_date))
    # assign the target table in a variable
    table_target = spark.read.parquet("wasbs://{}@{}.blob.core.windows.net/top_cineplex_rental/rentals-list-{}.parquet".format(container_name, storage_name, history))
    # full merge, join on key column and also high data column to make only join to the lastest records
    table_merge = table_target.join(table_source_new, (table_target.imdb_id == table_source_new.imdb_id) &
                                                      (table_target.end_date == table_source_new.src_end_date), how = 'fullouter' )

    #There are four possibilities for the actions:
        # UPSERT: attributes have changed in the source and the existing records need to be expired and new records need to be inserted.
        # NOTCURRENT: record is changed in source table and the records in target table need to be updated logically.
        # INSERT: new records exist in source that need to be inserted into the target table directly.
        # NOACTION: no changes to the attributes or the records in target table are not current.

    # derive new column to indicate the action
    table_merge = table_merge.withColumn( 'action',
                                        when(table_merge.title != table_merge.src_title, 'UPSERT' )
                                       .when(table_merge.src_imdb_id.isNull() & table_merge.is_current, 'NOTCURRENT')
                                       .when(table_merge.imdb_id.inNull(), 'INSERT')
                                       .otherwise('NOACTION')
                                        )
    table_merge.show()

    # for records that need no action
    table_merge_p1 = table_merge.filter(
                                        table_merge.action == 'NOACTION').select(column_names)

    # for records that need insert only
    table_merge_p2 = table_merge.filter(
                                        table_merge.action == 'INSERT').select(
                                            table_merge.src_imdb_id.alias('imdb_id'),
                                            table_merge.src_title.alias('title'),
                                            table_merge.ordering,
                                            lit(1).alias('is_current'),
                                            table_merge.src_start_date.alias('start_date'),
                                            table_merge.src_end_date.alias('end_date')
                                             )
    # for the records that are not current
    table_merge_p3 = table_merge.filter( 
                                        table_merge.action == 'NOTCURRENT').select(column_names).withColumn(
                                            'is_current', lit(0))

    # for the records that need to be set expired and then inserted
    table_merge_p4_1 = table_merge.filter(
                                        table_merge.action == 'UPSERT').select(
                                            table_merge.src_imdb_id.alias('imdb_id'),
                                            table_merge.src_title.alias('title'),
                                            table_merge.ordering,
                                            lit(1).alias('is_current'),
                                            table_merge.src_start_date.alias('start_date'),
                                            table_merge.src_end_date.alias('end_date')
                                        )
    table_merge_p4_2 = table_merge.filter(
                                        table_merge.action == 'UPSERT').withColumn(
                                            'end_date', date_sub(table_merge.src_start_date, 1)).withColumn(
                                            'is_current', lit(0)).select(column_names)
    # union all records together
    table_merge_final = table_merge_p1.unionAll(table_merge_p2).unionAll(
                            table_merge_p3).unionAll(table_merge_p4_1).unionAll(table_merge_p4_2)

    table_merge_final.withColumn('rental_id', row_number().over(Window.orderBy(monotonically_increasing_id()))).orderBy('start_date').show() # adding surrogate key

    # assign column names in order
    column_names = ['rental_id','imdb_id', 'title', 'ordering', 'is_current', 'start_date', 'end_date']
    table_merge_final.select(column_names)

    logger.info("Merged all the tables into dataframe")
    try:
        table_merge_final.write.parquet("wasbs://{}@{}.blob.core.windows.net/top_cineplex_rental/{}.parquet".format(container_name, storage_name,directory_1[-27:-4])) # eg: directory_1[-27:-4] is 'rentals-list-2022-04-21'
        logger.info("Moved %s.parquet to azure 'top_cineplex_rental' blob"%(directory_1[-27:-4]))
    except Exception as err:
        logger.warning("A warning message: {}".format(err))

else:
    # change the column names
    table_source = table_source.select(
                                       table_source.src_imdb_id.alias("imdb_id"),
                                       table_source.src_title.alias("title"),
                                       table_source.ordering)
    # add the column names and values
    table_source = table_source.withColumn('is_current', lit(1)).withColumn(
                                            'start_date', lit(current_date)).withColumn(
                                            'end_date', lit(high_date)).withColumn(
                                            'rental_id', row_number().over(Window.orderBy(monotonically_increasing_id()))) # adding surrogate key
    # assign column names in order
    column_names = ['rental_id','imdb_id', 'title', 'ordering', 'is_current', 'start_date', 'end_date']
    table_source.select(column_names)

    logger.info("Added first data into dataframe")
    # transfer csv file into parquet and save to azure blob storage
    try:
        table_source.write.parquet("wasbs://{}@{}.blob.core.windows.net/top_cineplex_rental/{}.parquet".format(container_name, storage_name,directory_1[-27:-4])) # eg: directory_1[-27:-4] is 'rentals-list-2022-04-21'
        logger.info("Moved %s.parquet to azure 'top_cineplex_rental' blob"%(directory_1[-27:-4]))
    except Exception as err:
        logger.warning("A warning message: {}".format(err))