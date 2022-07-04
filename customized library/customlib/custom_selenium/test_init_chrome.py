
from init_chrome import init_chrome_browser
import unittest
import unittest.mock
import io
from datetime import date

mock_stdout = unittest.mock.patch('sys.stdout', new_callable = io.StringIO )


class TestInitChrome(unittest.TestCase):
    
    @mock_stdout
    def test_init_chrome(self,stdout):
        url = "https://store.cineplex.com/collection2017?type=Top%20Rentals"
        chrome_driver_path = "/Volumes/Moon/SpringBoard/Top Rentals Cineplex/Data Collecting/chrome driver/chromedriver"
        download_path = "/mnt/container-data/"
        
        init_chrome_browser(download_path, chrome_driver_path, url)
        actual = stdout.getvalue()
        self.assertEqual(actual, f"{date.today()}    Launching Chrome...\n{date.today()}    Chrome launched.\n{date.today()}    Browser ready to use.\n")

if __name__ == '__main__':
    unittest.main()