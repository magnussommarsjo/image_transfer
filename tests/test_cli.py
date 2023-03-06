from pathlib import Path

import pytest

from typer.testing import CliRunner
from imgtrf.cli import app

runner = CliRunner()


def test_copy(temp_directory: Path):
    src_path = temp_directory / "source"
    dest_path = temp_directory / "destination"
    result = runner.invoke(app, ["copy", str(src_path), str(dest_path)])
    assert result.exit_code == 0
    assert (
        temp_directory / "destination" / "2020" / "01" / "01" / "file01.jpg"
    ).exists()


def test_copy_format(temp_directory: Path):
    src_path = temp_directory / "source"
    dest_path = temp_directory / "destination"
    result = runner.invoke(
        app, ["copy", "--dir-format", "Y/m", str(src_path), str(dest_path)]
    )
    assert result.exit_code == 0
    assert (temp_directory / "destination" / "2020" / "01" / "file01.jpg").exists()


def test_copy_not_a_directory(temp_directory: Path):
    src_path = temp_directory / "not-exists"
    dest_path = temp_directory / "destination"

    result = runner.invoke(app, ["copy", str(src_path), str(dest_path)])

    assert result.exit_code == 1


def test_move(temp_directory: Path):
    src_path = temp_directory / "source"
    dest_path = temp_directory / "destination"
    result = runner.invoke(app, ["move", str(src_path), str(dest_path)])
    assert result.exit_code == 0
    assert (
        temp_directory / "destination" / "2020" / "01" / "01" / "file01.jpg"
    ).exists()
    assert not (temp_directory / "source" / "file01.jpg").exists()


def test_move_format(temp_directory: Path):
    src_path = temp_directory / "source"
    dest_path = temp_directory / "destination"
    result = runner.invoke(
        app, ["move", "--dir-format", "Y/m", str(src_path), str(dest_path)]
    )
    assert result.exit_code == 0
    assert (temp_directory / "destination" / "2020" / "01" / "file01.jpg").exists()
    assert not (temp_directory / "source" / "file01.jpg").exists()


def test_remove_empty(temp_directory: Path):
    """Checks that we remove only empty directories"""
    src_path = temp_directory / "source"
    dir_to_be_removed = src_path / "to_be_removed" 
    sub_dir_to_be_removed = dir_to_be_removed / "sub_dir"
    sub_dir_to_be_removed.mkdir(parents=True)
    assert sub_dir_to_be_removed.exists()

    result = runner.invoke(app, ["remove", "dirs", str(src_path)])

    assert result.exit_code == 0

    assert not dir_to_be_removed.exists()
    assert (temp_directory / "source").exists()
    assert (temp_directory / "source" / "subfolder").exists()
    assert (temp_directory / "destination").exists()