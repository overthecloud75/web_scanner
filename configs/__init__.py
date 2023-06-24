import os

# log
BASE_DIR= os.getcwd()
LOG_DIR = 'logs'
LOG_FILE = LOG_DIR + '/webscanner.log'

# proxy
MITMPROXY = {'host': 'localhost', 'port': 8080}
