from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from configs import LOG_FILE, MITMPROXY

class Browser():

    def __init__(self, set_proxy=False):

        # selenuim 설정 
        options = Options()
        options.add_argument('--headless')
        options.add_argument('--log-path={}'.format(LOG_FILE))
        if set_proxy:
            options.add_argument('--proxy-server={}:{}'.format(MITMPROXY['host'], MITMPROXY['port']))
        options.add_argument('--ignore-certificate-errors')
        self.driver = webdriver.Chrome(options=options)
        self.driver.implicitly_wait(10)
        
   