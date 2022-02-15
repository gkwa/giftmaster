import argparse
import logging
import re
import sys

from giftmaster import args as argsmod
from giftmaster import logger as loggermod

"""
https://stackoverflow.com/a/48503066/16564820
"""


class SensitiveFormatter(logging.Formatter):
    """Formatter that removes sensitive information in signtool command logs."""

    @staticmethod
    def _filter(s):
        return re.sub(r"/kc +[^ ]+", r"/kc [MASKED]", s)

    def format(self, record):
        original = logging.Formatter.format(self, record)
        return self._filter(original)


def setup_logging(loglevel):
    """Setup basic logging

    Args:
      loglevel (int): minimum loglevel for emitting messages
    """
    logformat = "[%(asctime)s] %(levelname)s:%(name)s:%(message)s"
    logformat = "{%(filename)s:%(lineno)d} %(levelname)s - %(message)s"
    logging.basicConfig(
        level=loglevel, stream=sys.stdout, format=logformat, datefmt="%Y-%m-%d %H:%M:%S"
    )

    # Don't actually configure your logging like this, just to showcase
    # the above answer. :)
    for handler in logging.root.handlers:
        handler.setFormatter(SensitiveFormatter(logformat))


def main(args):
    parser = argparse.ArgumentParser()
    argsmod.add_common_args(parser)
    args = parser.parse_args()
    loggermod.setup_logging(args.loglevel)
    logging.debug("/kc secret /n")


def run():
    main(sys.argv[1:])


if __name__ == "__main__":
    run()
