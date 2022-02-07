import logging
import pathlib
import shutil
from typing import List

import pytest

from giftmaster import signtool, skeleton

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
    signtool_candidates = [
        r"C:\Program Files*\Windows Kits\*\bin\*\x64\signtool.exe",
        r"C:\Program*\Windows*\*\*\*\x64\signtool.exe",
    ]

    # capsys is a pytest fixture that allows asserts agains stdout/stderr
    # https://docs.pytest.org/en/stable/capture.html
    skeleton.main([file_list, "--signtool", signtool_candidates])
    # captured = capsys.readouterr()
    # assert "The 7-th Fibonacci number is 13" in captured.out
