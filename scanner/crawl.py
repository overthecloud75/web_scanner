from bs4 import BeautifulSoup
from urllib.parse import urljoin
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time

from configs import LOG_FILE, MITMPROXY 
from .mitm_log import MitmLogCheck

class Crawl():

    def __init__(self, start_url, logger):
        self.logger = logger
        self.logger.info('{} start'.format(__name__))

        self.start_url = start_url
        self.urls = [start_url]      # 수집한 URL을 저장할 리스트
        self.results = {}            # response 결과 저장 

        # Mitm 실행
        MitmLogCheck(self.start_url, logger, self.results)

        # selenuim 설정 
        options = Options()
        options.add_argument('--headless')
        options.add_argument('--log-path={}'.format(LOG_FILE))
        options.add_argument('--proxy-server={}:{}'.format(MITMPROXY['host'], MITMPROXY['port']))
        options.add_argument('--ignore-certificate-errors')
        self.driver = webdriver.Chrome(options=options)
        self.driver.implicitly_wait(10)
        
        self.collect_urls()
        time.sleep(3)

    def collect_urls(self):
        '''
            get_href : gather urls with a link
        '''

        # 이미 방문한 URL을 추적하기 위한 집합
        visited = set()

        # 시작 URL을 큐에 추가
        self.queue = [self.start_url]

        while self.queue:
            # 큐에서 URL을 가져옴
            url = self.queue.pop(0)
            if url not in visited:
                try:
                    self.driver.get(url)
                    page_source = self.driver.page_source
            
                    soup = BeautifulSoup(page_source, 'html.parser')
                    
                    self.get_a_link(url, soup)
                    # self.get_src(url, soup)

                    visited.add(url)

                except Exception as e:
                    self.logger.error('An error occurred: {}'.format(e))

        return visited

    def get_a_link(self, url, soup):
        '''
            ToDo : query에 대한 key 값을 저장
        '''
        # 현재 페이지에서 모든 링크를 찾음
        for link in soup.find_all('a'):
            href = link.get('href')
            self.get_url(url, href)

    def get_src(self, url, soup):
        
        # 현재 페이지에서 모든 링크를 찾음
        for link in soup.find_all('script'):
            href = link.get('src')
            self.get_url(url, href)
    
    def get_url(self, url, href):
        if href and (href.startswith('/') or href.startswith('http') or href.startswith('../')):
            if '?' in href:
                href = href.split('?')[0]
            self.logger.info('href: {}'.format(href))
            # 상대 URL을 절대 URL로 변환
            absolute_url = urljoin(url, href)
            # 도메인이 일치하는 경우에만 URL을 추가
            if absolute_url.startswith(self.start_url):
                self.urls.append(absolute_url)
                # 큐에 추가
                self.queue.append(absolute_url)

