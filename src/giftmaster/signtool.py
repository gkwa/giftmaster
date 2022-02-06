import logging
import pathlib
import subprocess
from typing import List

from foodsale import pathfromglob

from giftmaster import timestamp


class SignTool:
    HASH_ALGORITHM = "SHA256"
    url_manager = timestamp.TimeStampURLManager()

    def __init__(self, files_to_sign):
        paths = pathfromglob.abspathglob(
            r"C:\Program Files*\Windows Kits\*\bin\*\x64\signtool.exe"
        )
        assert len(paths) == 1
        signtool_path = paths[0]
        assert signtool_path.exists()
        self.files_to_sign = files_to_sign
        self.signtool_path = signtool_path
        logging.debug("signtool path: {}".format(signtool_path))

    @classmethod
    def from_list(cls, paths: List[pathlib.Path], dry_run=False):
        logging.debug("sign() called")
        tool = cls(paths)
        if not dry_run:
            tool.run(tool.sign_cmd())
        return tool

    def run(self, cmd):
        """
        python subprocess spaces path
        """
        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        log_path = pathlib.Path(f"signtool.log")
        err_path = pathlib.Path(f"signtool.err")
        stdout, stderr = process.communicate()
        err_path.write_text(stderr.decode())
        log_path.write_text(stdout.decode())
        logging.debug(stderr)

    def verify_cmd(self):
        prefix = [
            str(self.signtool_path),
            "verify",
            "/v",
        ]

        x = ["/pa"]
        x.extend(self.files_to_sign)

        cmd = []
        cmd.extend(prefix)
        cmd.extend(x)

        return cmd

    def sign_cmd(self):
        cmd = [
            str(self.signtool_path),
            "sign",
            "/v",
            "/n",
            "streambox",
            "/s",
            "My",
            "/fd",
            type(self).HASH_ALGORITHM,
            "/d",
            "spectra",
            "/tr",
            type(self).url_manager.url,
            "/td",
            type(self).HASH_ALGORITHM,
        ]

        cmd.extend(self.files_to_sign)

        return cmd


def main():
    files_to_sign = ["a.exe", "b.exe"]
    tool = SignTool.from_list(files_to_sign, dry_run=False)

    logging.debug("cmd: {}".format(tool.sign_cmd()))
    logging.debug("cmd: {}".format(tool.verify_cmd()))


if __name__ == "__main__":
    main()
