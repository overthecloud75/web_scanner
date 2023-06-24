import requests

class CheckConfig():

    def __init__(self, url, logger):
        self.logger = logger

        self.url = url
        self.results = {}

        self.scan()

    def scan(self):
        '''
            trace_method 
        '''
        self.check_trace_method()

    def check_trace_method(self):
        # https://portswigger.net/kb/issues/00500a00_http-trace-method-is-enabled
        try:
            response = requests.request('TRACE', self.url, verify=False)
            if response.status_code in [405, 501]:
                self.results['trace'] = {'result': 'ok', 'proof': 'status_code is {}'.format(response.status_code)}
            else:
                self.results['trace'] = {'result': 'fail', 'proof': 'status_code is {}'.format(response.status_code)}
        except Exception as e:
            self.logger.error('An error occurred: {}'.format(e))



        

   

