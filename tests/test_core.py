from pathlib import Path
from datetime import datetime

import pytest

from imgtrf import core


def test_copy_files(temp_directory: Path):
    src_dir = temp_directory / "source"
    dest_dir = temp_directory / "destination"

    core.copy_files(src_dir=src_dir, dest_dir=dest_dir, dir_format="%Y/%m/%d")

    assert (
        temp_directory / "destination" / "2020" / "01" / "01" / "file01.jpg"
    ).exists()

    assert (temp_directory / "source" / "file01.jpg").exists()
    assert (temp_directory / "source" / "subfolder" / "file02.jpg").exists()


def test_move_files(temp_directory: Path):
    src_dir = temp_directory / "source"
    dest_dir = temp_directory / "destination"

    core.move_files(src_dir=src_dir, dest_dir=dest_dir, dir_format="%Y/%m/%d")

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


def test_remove_dirs(tmp_path: Path):
    # Create empty
    empty_path = tmp_path / "to_remove" / "empty" / "subfolder"
    empty_path.mkdir(parents=True)
    assert empty_path.exists()
    
    # Create non-empty
    not_empty = tmp_path / "to_remove" / "not_empty" / "subfolder"
    not_empty.mkdir(parents=True)
    file = not_empty / "file.txt"
    file.write_text('NOT TO BE REMOVED')
    assert file.exists() and file.is_file()

    core.remove_dirs(tmp_path / "to_remove")

    assert not_empty.exists()
    assert not empty_path.exists()
    
    
def test_remove_dirs_cwd(monkeypatch: pytest.MonkeyPatch, tmp_path: Path):
    """Test that we skip removing the current working directory"""

    empty_path: Path = tmp_path / "empty"
    sub_folder = empty_path / "subfolder" / "subfolder2"
    sub_folder.mkdir(parents=True)

    monkeypatch.chdir(empty_path)
    assert Path.cwd() == empty_path

    core.remove_dirs(Path('.'))
    assert empty_path.exists()  # cwd should not be removed
    assert len([c for c in empty_path.iterdir()]) == 0 # empty
