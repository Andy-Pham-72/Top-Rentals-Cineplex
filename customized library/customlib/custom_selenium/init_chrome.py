from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from datetime import date


def init_chrome_browser(download_path, chrome_driver_path, url):
    """
    Initializes a Chrome browser.

    :param download_path: str
        The download path to place files downloaded from this browser session.
    :param chrome_driver_path : str
        The path of the chrome driver executable binary (.exe file).
    :param url : str
        The URL address of the page to initially load.

    :return:
        The initiated browser object.
    """

    options = Options()
    prefs = {'download.default_directory' : download_path}
    options.add_experimental_option('prefs', prefs)
    options.add_argument('--no-sandbox')
    options.add_argument('--headless')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--start-maximized')
    options.add_argument('window-size=2560,1440')
    print(f"{date.today()}    Launching Chrome...")
    browser = webdriver.Chrome(chrome_driver_path, options=options)
    print(f"{date.today()}    Chrome launched.")
    browser.get(url)
    print(f"{date.today()}    Browser ready to use.")
    return browser




