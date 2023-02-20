from datetime import datetime

import pytest

from typer.testing import CliRunner
from imgtrf.cli import app
from pathlib import Path

runner = CliRunner()

def create_file(directory: Path, file_name: str, creation_date: datetime):
    file = directory / file_name
    file.write_text('DUMMY_DATA')
    # ToDo
    # - Add creation date to file
    # - Use pillow to add metadata? 


@pytest.fixture
def temp_directory(tmp_path: Path) -> Path:

    # Create folders
    src = tmp_path / "source"
    src_subfolder = src / "subfolder"
    src.mkdir()
    src_subfolder.mkdir()
    dest = tmp_path / "destination"
    dest.mkdir()

    # Create files
    create_file(src, "file01.jpg", datetime(2020, 1, 1, 12, 00))
    create_file(src_subfolder, "file02.jpg", datetime(2020, 2, 1, 12, 00))

    yield tmp_path


def test_copy(temp_directory: Path):
    src_path = temp_directory / "source"
    dest_path = temp_directory / "destination"
    result = runner.invoke(app, ["copy", str(src_path), str(dest_path)])
    assert result.exit_code == 0
    assert (temp_directory / "destination" / "2020" / "01" / "01" / "file01.jpg").exists()
    

def test_copy_not_a_directory(temp_directory: Path):
    src_path = temp_directory / "not-exists"
    dest_path = temp_directory / "destination"
    
    result = runner.invoke(app, ["copy", str(src_path), str(dest_path)])

    assert result.exit_code == 1
    