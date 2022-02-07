import logging
import pathlib
import subprocess
from typing import List

from foodsale import pathfromglob

from giftmaster import timestamp


def get_abs_path(file_list: List) -> List[pathlib.Path]:
    return [str(pathlib.Path(_str).resolve()) for _str in file_list]


class SignTool:
    HASH_ALGORITHM = "SHA256"
    url_manager = timestamp.TimeStampURLManager()

    def set_path(self, globs: List[str]):
        def validate(globs):
            paths = pathfromglob.abspathglob(*globs)
            if len(paths) < 1:
                msg = f"no glob from list {globs} matche any paths on filesystem"
                logging.exception(msg)
                raise ValueError(msg)

            path = paths[0]

            if len(paths) > 1:
                msg = (
                    f"globs {globs} match too many paths on filesystem: {paths}.  "
                    "Not sure i'm choosing the one you want, namely {path}.  Its "
                    "the first one in the list"
                )
                logging.warning(msg)

            if not path.exists():
                msg = f"{path} does not exist"
                logging.exception(msg)
                raise ValueError(msg)

            return path

        self.path = validate(globs)

    def __init__(self, files_to_sign):
        self.files_to_sign = get_abs_path(files_to_sign)

    @classmethod
    def from_list(cls, paths: List[str], signtool: List[str], dry_run=False):
        tool = cls(paths)
        tool.set_path(signtool)
        if not dry_run:
            tool.run(tool.sign_cmd())
        return tool

    def run(self, cmd):
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
        logging.warning(stderr.decode())

    def verify_cmd(self):
        prefix = [
            str(self.path),
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

        cmd.extend(self.files_to_sign)

        return cmd


def main():
    pass


if __name__ == "__main__":
    main()
