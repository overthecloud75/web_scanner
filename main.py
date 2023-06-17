import argparse

from scanner import Scanner

parser = argparse.ArgumentParser()
parser.add_argument('-u', '--url', dest='url', action='store', required=True)   

def main(args):
    scan = Scanner(args)

if __name__ == '__main__':
    args = parser.parse_args()
    main(args)