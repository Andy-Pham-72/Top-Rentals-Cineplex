import os
import time
import csv

# web scrapper modules
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

# check for directories existence
if not os.path.isdir('/Volumes/Moon/SpringBoard/Top Rentals Cineplex/Data Collecting/cineplex dataset/top_rental_data'):
    os.makedirs('/Volumes/Moon/SpringBoard/Top Rentals Cineplex/Data Collecting/cineplex dataset/top_rental_data')

# download url
url = 'https://store.cineplex.com/collection2017?type=Top%20Rentals'

# path to the chrome driver
chrome_path = '/Volumes/Moon/SpringBoard/Top Rentals Cineplex/Data Collecting/chromedriver'

# set proxy to prevent selenium detector
PROXY = "23.23.23.23:3128" # IP:PORT or HOST:PORT
capabilities = dict(DesiredCapabilities.CHROME)
capabilities['proxy'] = {'proxyType': 'MANUAL','httpProxy': '23.23.23.23:3128','ftpProxy': '23.23.23.23:3128','sslProxy': '23.23.23.23:3128','noProxy': '','class': "org.openqa.selenium.Proxy",'autodetect': False}
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
    WebDriverWait(driver, timeout).until(EC.visibility_of_element_located((By.XPATH, "//*[@id='movie-collections-grid']/div[2]/div")))
except TimeoutException:
    print("Timed out waiting for page to load")

# get all the top rental links using list comprehension combined with selenium
titles_links = [item.get_attribute("href") for item in WebDriverWait(driver, timeout).until(EC.presence_of_all_elements_located((By.CLASS_NAME,"movie-pdp-link")))]

# create class to store data
class Rental(object):
    '''
    Class Rental to store "title", "year", "synopsis" data
    '''
    def __init__(self, title, year, synopsis):
        self.title = title
        self.year = year
        self.synopsis = synopsis

# create empty list    
rentals = []

# append data into the list
for link in titles_links:
    driver.get(link)
    print(f'downloading: {link} .......')
    try:
        title = WebDriverWait(driver, timeout).until(EC.visibility_of_element_located((By.XPATH, "//*[@id='main-content']/div[3]/div[1]/div/div[3]/div/div[1]/div[1]/span"))).text
        year  = WebDriverWait(driver, timeout).until(EC.visibility_of_element_located((By.XPATH, "//*[@id='main-content']/div[3]/div[1]/div/div[3]/div/div[1]/div[3]/span"))).text
        synopsis = WebDriverWait(driver, timeout).until(EC.visibility_of_element_located((By.XPATH, "//*[@id='main-content']/div[3]/div[1]/div/div[3]/div/div[5]/div/div/span[1]"))).text 
        time.sleep(5)
    except TimeoutException:
        synopsis = WebDriverWait(driver, timeout).until(EC.visibility_of_element_located((By.XPATH, "//*[@id='main-content']/div[3]/div[1]/div/div[3]/div/div[6]/div/div/span[1]"))).text 
    rentals.append(Rental(title, year, synopsis))

def save_rentals_to_csv_file(rentals_list, file_name):
    """
    function to write csv "rentals" variable to csv file
    """
    with open(file_name, 'w') as csvfile:
        fieldnames = ['title', 'year', 'synopsis']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        
        for rental in rentals_list:
            
            writer.writerow({'title' : rental.title, 'year' : rental.year, 'synopsis' : rental.synopsis })

# write csv file            
save_rentals_to_csv_file(rentals_list = rentals, file_name = "/Volumes/Moon/SpringBoard/Top Rentals Cineplex/Data Collecting/cineplex dataset/rentals_list.csv")

# close browser
driver.quit()