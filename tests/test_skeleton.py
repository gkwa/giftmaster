import pathlib
import shutil
from typing import List

import pytest

from giftmaster import skeleton

__author__ = "Taylor Monacelli"
__copyright__ = "Taylor Monacelli"
__license__ = "MPL-2.0"


@pytest.fixture
def large_file_list() -> List[str]:
    scratch = pathlib.Path("scratch")
    scratch.mkdir(parents=True, exist_ok=True)

    lst2 = []
    lst = list(pathlib.Path(r"C:\Windows\System32").rglob("*.exe"))
    for path in lst[:100000]:
        new = scratch / path.name
        shutil.copy(path, new)
        lst2.append(new)

    return [str(path) for path in lst2]


@pytest.fixture
def small_file_list() -> List[pathlib.Path]:
    return [
        r"C:\Windows\System32\a.exe",
        r"C:\Windows\System32\b.exe",
    ]


def test_main_without_batches(large_file_list):
    # capsys is a pytest fixture that allows asserts agains stdout/stderr
    # https://docs.pytest.org/en/stable/capture.html
    candidates = [
        r"C:\Program Files*\Windows Kits\*\bin\*\x64\signtool.exe",
        r"C:\Program*\Windows*\*\*\*\x64\signtool.exe",
    ]
    skeleton.main(
        [
            *large_file_list,
            "--batch-size",
            "0",
            "--signtool",
            *candidates,
        ]
    )
    # captured = capsys.readouterr()
    # assert "The 7-th Fibonacci number is 13" in captured.out


def test_main_batch_size(large_file_list):
    # capsys is a pytest fixture that allows asserts agains stdout/stderr
    # https://docs.pytest.org/en/stable/capture.html
    candidates = [
        r"C:\Program Files*\Windows Kits\*\bin\*\x64\signtool.exe",
        r"C:\Program*\Windows*\*\*\*\x64\signtool.exe",
    ]
    skeleton.main(
        [
            *large_file_list,
            "--signtool",
            *candidates,
            "--batch-size",
            "10",
        ]
    )
    # captured = capsys.readouterr()
    # assert "The 7-th Fibonacci number is 13" in captured.out


def test_main_default_signtool_makes_simple_invocation(small_file_list):
    # capsys is a pytest fixture that allows asserts agains stdout/stderr
    # https://docs.pytest.org/en/stable/capture.html
    skeleton.main(
        [
            *small_file_list,
            "--batch-size",
            "10",
        ]
    )
    # captured = capsys.readouterr()
    # assert "The 7-th Fibonacci number is 13" in captured.out
