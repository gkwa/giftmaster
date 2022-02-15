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

import logging
import sys

from giftmaster import __version__
from giftmaster import args as argsmod
from giftmaster import logger, signtool

__author__ = "Taylor Monacelli"
__copyright__ = "Taylor Monacelli"
__license__ = "MPL-2.0"

_logger = logging.getLogger(__name__)




def main(args):
    """Wrapper allowing :func:`fib` to be called with string arguments in a CLI fashion

    Instead of returning the value from :func:`fib`, it prints the result to the
    ``stdout`` in a nicely formatted message.

    Args:
      args (List[str]): command line parameters as list of strings
          (for example  ``["--verbose", "42"]``).
    """
    args = argsmod.parse_args(args)
    logger.setup_logging(args.loglevel)

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
    run()
