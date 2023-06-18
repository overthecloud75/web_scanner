import argparse

from scanner import Scanner

parser = argparse.ArgumentParser()
parser.add_argument('-d', '--domain', dest='domain', required=True)

def main(args):
    scan = Scanner(args)

if __name__ == '__main__':
    args = parser.parse_args()
    main(args)