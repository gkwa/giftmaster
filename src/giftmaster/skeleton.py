"""
This is a skeleton file that can serve as a starting point for a Python
console script. To run this script uncomment the following lines in the
``[options.entry_points]`` section in ``setup.cfg``::

    console_scripts =
         fibonacci = giftmaster.skeleton:run

Then run ``pip install .`` (or ``pip install -e .`` for editable mode)
which will install the command ``fibonacci`` inside your current environment.

Besides console scripts, the header (i.e. until ``_logger``...) of this file can
also be used as template for Python modules.

Note:
    This skeleton file can be safely removed if not needed!

References:
    - https://setuptools.pypa.io/en/latest/userguide/entry_point.html
    - https://pip.pypa.io/en/stable/reference/pip_install
"""

import argparse
import logging
import sys

from giftmaster import __version__, signtool

__author__ = "Taylor Monacelli"
__copyright__ = "Taylor Monacelli"
__license__ = "MPL-2.0"

_logger = logging.getLogger(__name__)


# ---- CLI ----
# The functions defined in this section are wrappers around the main Python
# API allowing them to be called directly from the terminal as a CLI
# executable/script.


def check_positive(value):
    ivalue = int(value)
    if ivalue <= 0:
        raise argparse.ArgumentTypeError(f"{value} is an invalid positive int value")
    return ivalue


def parse_args(args):
    """Parse command line parameters

    Args:
      args (List[str]): command line parameters as list of strings
          (for example  ``["--help"]``).

    Returns:
      :obj:`argparse.Namespace`: command line parameters namespace
    """
    parser = argparse.ArgumentParser(description="Just a Fibonacci demonstration")
    parser.add_argument(
        "--dry-run",
        action="store_true",
        default=False,
        help="don't actually run signtool if using --dry-run bool",
    )
    parser.add_argument(
        "--version",
        action="version",
        version="giftmaster {ver}".format(ver=__version__),
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
        "-b",
        "--batch-size",
        help="instead of signing all files at once, sign in batches of --batch-size",
        default=0,
        type=int,
    )
    return parser.parse_args(args)


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


def main(args):
    """Wrapper allowing :func:`fib` to be called with string arguments in a CLI fashion

    Instead of returning the value from :func:`fib`, it prints the result to the
    ``stdout`` in a nicely formatted message.

    Args:
      args (List[str]): command line parameters as list of strings
          (for example  ``["--verbose", "42"]``).
    """
    args = parse_args(args)
    setup_logging(args.loglevel)

    _logger.debug(f"file list {args.files}")

    file_list = args.files

    if not file_list:
        return

    _logger.debug(f"file list length: {len(file_list):,d}")
    signtool_candidates = args.signtool

    batch_size = len(args.files) if not args.batch_size else args.batch_size
    batches = [
        file_list[i : i + batch_size] for i in range(0, len(file_list), batch_size)
    ]
    _logger.debug(
        f"there are {len(batches):,d} batch(s), with most having length {len(batches[0]):,d}"
    )

    for batch in batches:
        tool = signtool.SignTool.from_list(
            batch,
            signtool=signtool_candidates,
        )
        if not args.dry_run:
            tool.remove_already_signed()
            tool.run(tool.sign_cmd())

    _logger.info("Script ends here")


def run():
    """Calls :func:`main` passing the CLI arguments extracted from :obj:`sys.argv`

    This function can be used as entry point to create console scripts with setuptools.
    """
    main(sys.argv[1:])


if __name__ == "__main__":
    # ^  This is a guard statement that will prevent the following code from
    #    being executed in the case someone imports this file instead of
    #    executing it as a script.
    #    https://docs.python.org/3/library/__main__.html

    # After installing your project with pip, users can also run your Python
    # modules as scripts via the ``-m`` flag, as defined in PEP 338::
    #
    #     python -m giftmaster.skeleton 42
    #
    run()
