from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from datetime import datetime


def init_chrome_browser(download_path, chrome_driver_path, url):
    """
    Instatiates a Chrome browser.

    :param download_path: str
        The download path to place files downloaded from this browser session.
    :param chrome_driver_path : str
        The path of the chrome driver executable binary (.exe file).
    :param url : str
        The URL address of the page to initially load.

    :return:
        The instantiated browser object.
    """

    options = Options()
    prefs = {'download.default_directory' : download_path}
    options.add_experimental_option('prefs', prefs)
    options.add_argument('--no-sandbox')
    options.add_argument('--headless')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--start-maximized')
    options.add_argument('window-size=2560,1440')
    print(f"{datetime.now()}    Launching Chrome...")
    browser = webdriver.Chrome(service=Service(chrome_driver_path), options=options)
    print(f"{datetime.now()}    Chrome launched.")
    browser.get(url)
    print(f"{datetime.now()}    Browser ready to use.")
    return browser




