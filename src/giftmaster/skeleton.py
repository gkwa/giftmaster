import logging
import sys

from giftmaster import __version__
from giftmaster import args as argsmod
from giftmaster import logger, signtool

__author__ = "Taylor Monacelli"
__copyright__ = "Taylor Monacelli"
__license__ = "MPL-2.0"

_logger = logging.getLogger(__name__)


def client(file_list, signtool_candidates, batch_size, dry_run=None):
    if not file_list:
        return

    _logger.debug(f"file list length: {len(file_list):,d}")

    batch_size = len(file_list) if not batch_size else batch_size
    batches = [
        file_list[i : i + batch_size] for i in range(0, len(file_list), batch_size)
    ]
    _logger.debug(
        f"there are {len(batches):,d} batch(s), with most having length {len(batches[0]):,d}"
    )

    dry_run = dry_run

    for batch in batches:
        tool = signtool.SignTool.from_list(
            batch,
            signtool=signtool_candidates,
        )
        if not dry_run:
            tool.remove_already_signed()
            tool.run(tool.sign_cmd())

    _logger.info("Script ends here")


def main(args):
    args = argsmod.parse_args(args)
    logger.setup_logging(args.loglevel)

    _logger.debug(f"file list {args.files}")

    file_list = args.files

    if not file_list:
        return

    _logger.debug(f"file list length: {len(file_list):,d}")
    signtool_candidates = args.signtool

    batch_size = len(args.files) if not args.batch_size else args.batch_size
    client(file_list, signtool_candidates, batch_size, dry_run=args.dry_run)


def run():
    main(sys.argv[1:])


if __name__ == "__main__":
    run()
