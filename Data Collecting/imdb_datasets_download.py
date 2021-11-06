import os
import time

# web scrapper modules
from selenium import webdriver

# unzip modules
import gzip
import shutil

# check for directories existence
directory_0 = 'Data Collecting/imdb dataset/raw_data'
directory_1 = 'Data Collecting/imdb dataset/extracted_data'

if not os.path.isdir(directory_0):
    os.makedirs(directory_0)

if not os.path.isdir(directory_1):
    os.makedirs(directory_1)

def latest_download_file(path):
    """
    function to wait for pending downloads to finish 
    """
    os.chdir(path)
    files = sorted(os.listdir(os.getcwd()), key=os.path.getmtime)
    newest = files[-1]

    return newest

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
    print(f'downloading: {download_list[i]}.......')

# wait for all downloads to finish
fileends = "crdownload"
dir = r'/Volumes/Moon/SpringBoard/Top Rentals Cineplex/Data Collecting/imdb dataset/raw_data'
while "crdownload" == fileends:
    time.sleep(1)
    newest_file = latest_download_file(path = dir)
    if "crdownload" in newest_file:
        fileends = "crdownload"
    else:
        fileends = "none"

print('download complete!')

# unzip gz files
for i in range(len(download_list)):
    time.sleep(3)
    directory_2 = '/Volumes/Moon/SpringBoard/Top Rentals Cineplex/Data Collecting/imdb dataset/raw_data/'
    directory_3 = '/Volumes/Moon/SpringBoard/Top Rentals Cineplex/Data Collecting/imdb dataset/extracted_data/'
    with gzip.open( directory_2 + {download_list[i]} , 'rb') as f_in:
        with open( directory_3 + {download_list[i][:-3]} , 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)

# close browser
driver.quit()