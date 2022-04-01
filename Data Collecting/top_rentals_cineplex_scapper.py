import os
import time
import csv
import datetime

# config
from config import config_cineplex

# web scrapper modules
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

# config variable
my_config = config_cineplex()

# check for directories existence
directory_0 = my_config[0]

if not os.path.isdir(directory_0):
    os.makedirs(directory_0)

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
    """
    with open(file_name, 'w') as csvfile:
        fieldnames = ['title', 'year', 'synopsis']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        
        for rental in rentals_list:
            
            writer.writerow({'title' : rental.title, 'year' : int(rental.year), 'synopsis' : rental.synopsis })
            
# download url
url = my_config[2]

# path to the chrome driver
chrome_path = '/Volumes/Moon/SpringBoard/Top Rentals Cineplex/Data Collecting/chromedriver'

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
driver = webdriver.Chrome(chrome_path, options =chrome_options)
driver.get(url)

# set timeout
timeout = 5
try:
    xpath_movie_list = "//*[@id='movie-collections-grid']/div[2]/div"
    WebDriverWait(driver, timeout).until(EC.visibility_of_element_located((By.XPATH, xpath_movie_list)))
except TimeoutException:
    print("Timed out waiting for page to load")

# get all the top rental links using list comprehension combined with selenium
class_link = "movie-pdp-link"
titles_links = [item.get_attribute("href") for item in WebDriverWait(driver, timeout). \
                   until(EC.presence_of_all_elements_located((By.CLASS_NAME, class_link)))]

# create empty list    
rentals = []

# append data into the list
for link in titles_links:
    driver.get(link)
    print(f'downloading: {link} .......')
    try:
        xpath_title = "//*[@id='main-content']/div[3]/div[1]/div/div[3]/div/div[1]/h1/span"
        xpath_year = "//*[@id='main-content']/div[3]/div[1]/div/div[3]/div/div[1]/div[2]/span"
        xpath_synopsis_1 = "//*[@id='main-content']/div[3]/div[1]/div/div[3]/div/div[5]/div/div"
        xpath_synopsis_2 = "//*[@id='main-content']/div[3]/div[1]/div/div[3]/div/div[6]/div/div"
        
        # retrieve data
        title = WebDriverWait(driver, timeout).until(EC.visibility_of_element_located((By.XPATH, xpath_title))).text
        year  = WebDriverWait(driver, timeout).until(EC.visibility_of_element_located((By.XPATH, xpath_year))).text
        synopsis = WebDriverWait(driver, timeout).until(EC.visibility_of_element_located((By.XPATH, xpath_synopsis_1))).text 
        
        # slow down the execution
        time.sleep(5)

    except TimeoutException:
        # retrieve data due to different html setup
        synopsis = WebDriverWait(driver, timeout).until(EC.visibility_of_element_located((By.XPATH, xpath_synopsis_2))).text 
    
    # append data to rentals list
    rentals.append(Rental(title, year, synopsis))

# write csv file
directory_1 = my_config[1] + datetime.today().strftime("%Y%m%d")+ ".csv"            
save_rentals_to_csv_file(rentals_list = rentals, file_name = directory_1)

# close browser
driver.quit()