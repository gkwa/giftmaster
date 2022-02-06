import logging
import pathlib
import shutil
from typing import List

import pytest

from giftmaster import signtool

__author__ = "Taylor Monacelli"
__copyright__ = "Taylor Monacelli"
__license__ = "MPL-2.0"


@pytest.fixture
def file_list() -> List[pathlib.Path]:
    scratch = pathlib.Path("scratch")
    scratch.mkdir(parents=True, exist_ok=True)

    lst2 = []
    lst = list(pathlib.Path(r"C:\Windows\System32").glob("*.exe"))
    for path in lst[:1000]:
        new = scratch / path.name
        shutil.copy(path, new)
        lst2.append(new)

    return lst2


def test_main(file_list):
    files_to_sign = file_list
    tool = signtool.SignTool.from_list(
        files_to_sign,
        signtool=r"C:\Program*\Windows Kits\*\bin\*\x64\signtool.exe",
        dry_run=False,
    )

    logging.debug(f"{tool.sign_cmd()}")
    logging.debug(f"{tool.verify_cmd()}")

    # capsys is a pytest fixture that allows asserts agains stdout/stderr
    # https://docs.pytest.org/en/stable/capture.html
    # main(["7"])
    # captured = capsys.readouterr()
    # assert "The 7-th Fibonacci number is 13" in captured.out
