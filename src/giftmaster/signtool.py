import logging
import pathlib
import subprocess
import time
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
                    f"Not sure i'm choosing the one you want, namely {path}.  Its "
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
    def from_list(cls, paths: List[str], signtool: List[str]):
        tool = cls(paths)
        tool.set_path(signtool)
        return tool

    def remove_already_signed(self):
        for path in self.files_to_sign:
            logging.debug(f"path:{path}")
            ret = self.run(self.verify_cmd([path]))
            if ret == 0:
                lst = self.files_to_sign
                lst.remove(path)
                logging.debug(f"removing {path} from list of files to sign because {path} is already signed")
                self.files_to_sign = lst

    def run(self, cmd) -> int:
        try:
            logging.debug(" ".join(cmd))
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
        except FileNotFoundError as ex:
            logging.exception(ex)
            raise ex

        epoch = int(time.time())
        log_path = pathlib.Path(f"signtool-{epoch}.log")
        err_path = pathlib.Path(f"signtool-{epoch}.err")
        stdout, stderr = process.communicate()
        err_path.write_text(stderr.decode())
        log_path.write_text(stdout.decode())
        logging.warning(stderr.decode())
        
        logging.debug(f"returncode: {process.returncode}")
        return process.returncode

    def verify_cmd(self, paths: List[str]):
        prefix = [
            str(self.path),
            "verify",
            "/v",
        ]

        x = ["/pa"]
        x.extend(paths)

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
