from pathlib import Path
from datetime import datetime

import pytest

from imgtrf import core


def test_copy_files(temp_directory: Path):
    src_path = temp_directory / "source"
    dest_path = temp_directory / "destination"

    core.copy_files(src_path, dest_path)

    assert (
        temp_directory / "destination" / "2020" / "01" / "01" / "file01.jpg"
    ).exists()

    assert (temp_directory / "source" / "file01.jpg").exists()
    assert (temp_directory / "source" / "subfolder" / "file02.jpg").exists()


def test_move_files(temp_directory: Path):
    src_path = temp_directory / "source"
    dest_path = temp_directory / "destination"

    core.move_files(src_path, dest_path)

    assert (
        temp_directory / "destination" / "2020" / "01" / "01" / "file01.jpg"
    ).exists()

    assert not (temp_directory / "source" / "file01.jpg").exists()
    assert not (temp_directory / "source" / "subfolder" / "file02.jpg").exists()




@pytest.mark.parametrize(
    "dir_format,expected_path",
    [
        ("%Y/%m/%d", Path("2023/01/01")),
        ("Y/m/d", Path("2023/01/01")),
        ("Year-%Y/Month-%m/Day-%d", Path("Year-2023/Month-01/Day-01")),
        ("%Y/%Y-%m-%d", Path("2023/2023-01-01")),
        ("Y/Y-m-d", Path("2023/2023-01-01")),
        ("%A %B %Y", Path("Sunday January 2023")),
        ("A B Y", Path("Sunday January 2023")),
    ],
)
def test_create_path_from(dir_format: str, expected_path: Path):
    dt = datetime(2023, 1, 1, 12, 0)
    output = core._create_path_from(dt, dir_format)
    assert output == expected_path
