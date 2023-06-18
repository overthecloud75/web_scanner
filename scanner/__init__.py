import urllib3

from .configuration import CheckConfig
from .crawl import Crawl
from .port_scan import PortScan

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class Scanner():

    def __init__(self, args):
        self.domain = args.domain

        self.scan()

    def scan(self):
        '''
            port scan
            crawl urls 
            check configuration 
        '''

        port_scan = PortScan(domain=self.domain)

        start_url = ''

        if 443 in port_scan.live_ports:
            start_url = 'https://' + self.domain
        elif 80 in port_scan.live_ports:
            start_url =  'http://' + self.domain

        print('start_url', start_url)
        
        if start_url:
            crawl = Crawl(start_url)
            results = crawl.results
            for url in crawl.results:
                if url == start_url:
                    check_config = CheckConfig(url)
                    for config_key in check_config.results:
                        results[url][config_key] = check_config.results[config_key]

                print(url, results[url])






