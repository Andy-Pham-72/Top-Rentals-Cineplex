
from init_chrome import init_chrome_browser
import unittest
import unittest.mock
import io

class TestInitChrome(unittest.TestCase):
    
    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    def test_init_chrome(self, expected_output, mock_stdout):
        url = "https://store.cineplex.com/collection2017?type=Top%20Rentals"
        chrome_driver_path = "/tmp/chromedriver/chromedriver"
        download_path = "/mnt/container-data/"
        init_chrome_browser(download_path, chrome_driver_path, url)
        self.assertEqual(mock_stdout.getvalue(), expected_output)
        
if __name__ == '__main__':
    unittest.main()