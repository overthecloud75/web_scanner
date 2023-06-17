from .configuration import CheckConfig

class Scanner():

    def __init__(self, args):
        self.url = args.url
        self.scan()

    def scan(self):
        check_config = CheckConfig(self.url)
        check_config.scan() 


