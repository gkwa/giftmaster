import pathlib
import shutil

import pytest

from giftmaster.skeleton import fib

__author__ = "Taylor Monacelli"
__copyright__ = "Taylor Monacelli"
__license__ = "MPL-2.0"


def get_test_pathlist():
    scratch = pathlib.Path("scratch")
    scratch.mkdir(parents=True, exist_ok=True)
    lst = list(pathlib.Path(r"C:\Windows\System32").glob("*.exe"))
    lst2 = []
    for path in lst[:1000]:
        new = scratch / path.name
        shutil.copy(path, new)
        lst2.append(new)

    return lst2


def test_main(capsys):
    """CLI Tests"""
    pathlist = get_test_pathlist()
    # capsys is a pytest fixture that allows asserts agains stdout/stderr
    # https://docs.pytest.org/en/stable/capture.html
    # main(["7"])
    # captured = capsys.readouterr()
    # assert "The 7-th Fibonacci number is 13" in captured.out
