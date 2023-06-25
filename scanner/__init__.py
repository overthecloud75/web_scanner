import urllib3

from .configuration import CheckConfig
from .crawl import Crawl
from .port_scan import PortScan
from utils import setup_logger
from .broswer import Browser

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class Scanner():

    def __init__(self, args):
        self.logger = setup_logger()
        self.logger.info('{} start'.format(__name__))

        self.domain = args.domain
        self.scan()

    def scan(self):
        '''
            1. port scan
            2. crawl urls 
            3. execute web_driver 
            4. check configuration 
            5. check XSS
        '''
        # 1. port scan
        port_scan = PortScan(domain=self.domain, logger=self.logger)

        start_url = ''

        if 443 in port_scan.live_ports:
            start_url = 'https://' + self.domain
        elif 80 in port_scan.live_ports:
            start_url =  'http://' + self.domain

        self.logger.info('start_url: {}'.format(start_url))
        
        if start_url:
            # 2. crawl urls
            crawl = Crawl(start_url, logger=self.logger)
            crawl.collect_urls()
            results = crawl.results

            # 3. execute web driver 
            chrome_browser = Browser()
            self.driver = chrome_browser.driver
            
            for path in results:
                if path == start_url or path == '/':
                    # 4. check configuration 
                    check_config = CheckConfig(start_url, logger=self.logger)
                    for config_key in check_config.results:
                        results[path][config_key] = check_config.results[config_key]
                self.logger.info('{}: {}'.format(path, results[path]))
            
                query_exists = False
                if 'query_exists' in results[path]:
                    query_exists = results[path]['query_exists']
                else:
                    # css, js, image file 등에 query_exists key 값이 없음 
                    pass

                # if query_exists:
                #    self.logger.info('{}: {}'.format(path, results[path]))
            







