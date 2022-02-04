import logging
import pathlib
import subprocess

from giftmaster import pathfromglob, timestamp


class SignTool:
    HASH_ALGORITHM = "SHA256"
    url_manager = timestamp.TimeStampURLManager()

    def __init__(self, pathlist):
        self.logger = logging.getLogger(__name__)
        self.pathlist = pathlist
        candidates = r"""
        C:\Program Files*\Windows Kits\*\bin\*\x64\signtool.exe
        """
        path = pathfromglob.PathFromGlob.from_string(candidates).path
        self.path = path
        self.logger.debug("signtool path: {}".format(path))

    @classmethod
    def from_list(cls, paths, dry_run=False):
        logger = logging.getLogger(__name__)
        logger.debug("sign() called")
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
        self.logger.debug(stderr)

    def verify_cmd(self):
        # signtool.exe verify /v /pa C:\spectra_installer\installer\Work1\dist\SpectraControlPanel.exe
        prefix = [
            str(self.path),
            "verify",
            "/v",
        ]

        x = ["/pa"]
        x.extend(self.pathlist)

        cmd = []
        cmd.extend(prefix)
        cmd.extend(x)

        return cmd

    def sign_cmd(self):
        cmd = [
            str(self.path),
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

        cmd.extend(self.pathlist)

        return cmd


def main():
    tool = SignTool.from_list(pathlist, dry_run=False)

    logging.debug("cmd: {}".format(tool.sign_cmd()))
    logging.debug("cmd: {}".format(tool.verify_cmd()))


if __name__ == "__main__":
    main()
