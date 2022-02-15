import argparse
import logging

from giftmaster import __version__


def add_common_args(parser):
    parser.add_argument(
        "-v",
        "--verbose",
        dest="loglevel",
        help="set loglevel to INFO",
        action="store_const",
        const=logging.INFO,
    )
    parser.add_argument(
        "-vv",
        "--very-verbose",
        dest="loglevel",
        help="set loglevel to DEBUG",
        action="store_const",
        const=logging.DEBUG,
    )
    parser.add_argument(
        "--version",
        action="version",
        version="giftmaster {ver}".format(ver=__version__),
    )


def parse_args(args):
    """Parse command line parameters

    Args:
      args (List[str]): command line parameters as list of strings
          (for example  ``["--help"]``).

    Returns:
      :obj:`argparse.Namespace`: command line parameters namespace
    """
    parser = argparse.ArgumentParser(description="Just a Fibonacci demonstration")
    add_common_args(parser)
    parser.add_argument(
        "--dry-run",
        action="store_true",
        default=False,
        help="don't actually run signtool if using --dry-run bool",
    )
    parser.add_argument(
        "--signtool",
        nargs="*",
        default=[
            r"C:\Program Files*\Windows Kits\*\bin\*\x64\signtool.exe",
        ],
        help="list of absolute paths possibly containing wildcards that will match path to signtool.exe",
    )
    parser.add_argument(
        dest="files", help="list of absolue paths to files to sign", nargs="*"
    )
    parser.add_argument(
        "-b",
        "--batch-size",
        help="instead of signing all files at once, sign in batches of --batch-size",
        default=0,
        type=int,
    )
    return parser.parse_args(args)
