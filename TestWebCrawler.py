import unittest
from WebCrawler import getProfiles
from selenium import webdriver
from selenium.webdriver.common.by import By


class TestWebCrawler(unittest.TestCase):
    options = webdriver.ChromeOptions()
    options.add_argument("headless")
    browser = webdriver.Chrome(options=options)
    URL = "https://www.crudemonitor.ca/"

    def setUpClasss():
        TestWebCrawler.URL = URL
        TestWebCrawler.browser = browser

    def  test_title_text(self):
        print('---- Testing Page Title ----')
        TestWebCrawler.browser.execute_script("window.open('%s', '_self');" % TestWebCrawler.URL)
        pageTitle = TestWebCrawler.browser.execute_script("return document.getElementsByTagName('h1');")[0].text
        self.assertEqual('CrudeMonitor', pageTitle)

    def test_content_exists(self):
        print('---- Testing Content ----')
        TestWebCrawler.browser.execute_script("window.open('%s', '_self');" % TestWebCrawler.URL)
        content = TestWebCrawler.browser.find_elements(By.XPATH, "//div[@class='card home-card']")
        self.assertIsNotNone(content)


if __name__ == '__main__':
    unittest.main()