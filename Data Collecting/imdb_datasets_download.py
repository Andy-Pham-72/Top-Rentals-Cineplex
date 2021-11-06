import os
import time

# web scrapper modules
from selenium import webdriver

# unzip modules
import gzip
import shutil

# check for directories existence
if not os.path.isdir('Data Collecting/imdb dataset/raw_data'):
    os.makedirs('Data Collecting/imdb dataset/raw_data')

if not os.path.isdir('Data Collecting/imdb dataset/extracted_data'):
    os.makedirs('Data Collecting/imdb dataset/extracted_data')

# download url
url = 'https://datasets.imdbws.com'

# path to the chrome driver
chrome_path = 'Data Collecting/chromedriver'

# custom path to the download directory
download_dir = '/Volumes/Moon/SpringBoard/Top Rentals Cineplex/Data Collecting/imdb dataset/raw_data'
chrome_options = webdriver.ChromeOptions()
preferences = {"download.default_directory": download_dir ,
               "directory_upgrade": True,
               "safebrowsing.enabled": True }
chrome_options.add_experimental_option("prefs", preferences)

driver = webdriver.Chrome(chrome_path, chrome_options= chrome_options)
driver.get(url)

# list of files
download_list = ['title.akas.tsv.gz',
                 'title.basics.tsv.gz',
                 'title.crew.tsv.gz',
                 'title.principals.tsv.gz',
                 'title.ratings.tsv.gz',
                 'name.basics.tsv.gz']

# download raw files                 
for i in range(len(download_list)):
    driver.find_element_by_link_text(f'{download_list[i]}').click()

def latest_download_file():
    """
    function to wait for pending downloads to finish 
    """
    path = r'/Volumes/Moon/SpringBoard/Top Rentals Cineplex/Data Collecting/imdb dataset/raw_data'
    os.chdir(path)
    files = sorted(os.listdir(os.getcwd()), key=os.path.getmtime)
    newest = files[-1]

    return newest

# wait for all downloads to finish
fileends = "crdownload"
while "crdownload" == fileends:
    time.sleep(1)
    newest_file = latest_download_file()
    if "crdownload" in newest_file:
        fileends = "crdownload"
    else:
        fileends = "none"

# unzip gz files
for i in range(len(download_list)):
    time.sleep(3)
    with gzip.open(f'/Volumes/Moon/SpringBoard/Top Rentals Cineplex/Data Collecting/imdb dataset/raw_data/{download_list[i]}', 'rb') as f_in:
        with open(f'/Volumes/Moon/SpringBoard/Top Rentals Cineplex/Data Collecting/imdb dataset/extracted_data/{download_list[i][:-3]}', 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)