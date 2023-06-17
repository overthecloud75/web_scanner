import requests

class CheckConfig():

    def __init__(self, url):
        self.url = url
        self.config_results = {}

    def scan(self):
        '''
            server_info
            trace_method 
        '''

        self.check_trace_method()
        print(self.config_results)


    def check_server_info(self, headers):
        if 'Server' in headers and headers['Server']:
            if 'server' not in self.config_results:
                self.config_results['server'] = [headers['Server']]
            elif headers['Server'] not in self.config_results['server']:
                self.config_results['server'] = self.config_results['server'].append(headers['Server'])


    def check_trace_method(self):
        # https://portswigger.net/kb/issues/00500a00_http-trace-method-is-enabled
        try:
            res = requests.request('TRACE', self.url)
            self.check_server_info(res.headers)
            if res.status_code in [405, 501]:
                self.config_results['trace'] = {'result': 'ok', 'proof': 'status_code is {}'.format(res.status_code)}
            else:
                self.config_results['trace'] = {'result': 'fail', 'proof': 'status_code is {}'.format(res.status_code)}
        except Exception as e:
                print('An error occurred:', str(e))



        

   

