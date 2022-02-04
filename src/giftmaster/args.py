import argparse
import sys


def _error(parser):
    def wrapper(interceptor):
        parser.print_help()
        sys.exit(-1)

    return wrapper


parser = argparse.ArgumentParser()
parser.add_argument("-d", "--debug", default=False, action="store_true")
parser.error = _error(parser)
