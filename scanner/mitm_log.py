import json
import asyncio
import threading
from mitmproxy import proxy, options
from mitmproxy.tools.dump import DumpMaster
from urllib.parse import urlparse, parse_qs

from configs import MITMPROXY 
from utils import filter_url

class AddLog:
    def __init__(self, start_url, logger, results):
        self.logger = logger
        self.start_url = start_url
        self.results = results

    def request(self, flow):
        '''
            method: HTTP 요청 메서드를 나타내는 문자열입니다.
            url: 요청 URL을 나타내는 문자열입니다.
            headers: 요청 헤더를 나타내는 mitmproxy.net.http.Headers 객체입니다. 헤더는 사전과 유사한 인터페이스를 가지고 있습니다.
            content: 요청 본문을 나타내는 bytes 객체입니다.
            text: 요청 본문을 텍스트로 디코딩한 문자열입니다.
            http_version: 사용된 HTTP 버전을 나타내는 문자열입니다.
            timestamp_start: 요청 시작 시간을 나타내는 mitmproxy.net.http.Timestamp 객체입니다.
            timestamp_end: 요청 종료 시간을 나타내는 mitmproxy.net.http.Timestamp 객체입니다.
        '''
        
    def response(self, flow):
        '''
            status_code: 응답 상태 코드를 나타내는 정수 값입니다.
            headers: 응답 헤더를 나타내는 mitmproxy.net.http.Headers 객체입니다. 헤더는 사전과 유사한 인터페이스를 가지고 있습니다.
            content: 응답 본문을 나타내는 bytes 객체입니다.
            text: 응답 본문을 텍스트로 디코딩한 문자열입니다.
            http_version: 사용된 HTTP 버전을 나타내는 문자열입니다.
            is_replay: 응답이 재생되는 것인지 여부를 나타내는 부울 값입니다.
            timestamp_start: 응답 시작 시간을 나타내는 mitmproxy.net.http.Timestamp 객체입니다.
            timestamp_end: 응답 종료 시간을 나타내는 mitmproxy.net.http.Timestamp 객체입니다.
        '''
        headers_dict = dict(flow.request.headers.items())
        path, query, fragment = filter_url(flow.request.url)
        self.results[path] = {'method': flow.request.method, 'query': query, 'fragment': fragment, 'status_code': flow.response.status_code, 'headers': headers_dict}

class MitmLogCheck():

    def __init__(self, start_url, logger, results):
        self.logger = logger
        self.logger.info('{} start'.format(__name__))

        self.start_url = start_url
        self.results = results

        th = threading.Thread(target=self.start_mitm)
        th.daemon = True
        th.start()

    def start_mitm(self):
        asyncio.run(self.run())

    async def run(self):

        addons = [AddLog(self.start_url, self.logger, self.results)]

        # mitm proxy 설정
        mitm_options = options.Options(listen_host=MITMPROXY['host'], listen_port=MITMPROXY['port'], ssl_insecure=True) #, certs=['*=mitmproxy.pem'])
        dump = DumpMaster(mitm_options, with_termlog=False)
        dump.addons.add(*addons)
        await dump.run()

    
