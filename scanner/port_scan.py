import nmap

class PortScan():

    def __init__(self, domain, logger):
        self.logger = logger
        self.logger.info('{} start'.format(__name__))

        self.host = domain 
        self.ports = '80, 443'

        self.live_ports = []

        self.collect_ports()

    def collect_ports(self):

        scanner = nmap.PortScanner()
        scanner.scan(self.host, self.ports, arguments='-Pn')
        
        for target_host in scanner.all_hosts():
            self.logger.info('Scanning host: {}'.format(target_host))
            ports = list(scanner[target_host]['tcp'].keys())

            if not self.live_ports:
                self.live_ports = ports
            else:
                for port in ports:
                    if port not in self.live_ports:
                        self.live_ports.append(port)

