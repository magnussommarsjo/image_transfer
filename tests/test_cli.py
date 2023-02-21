from pathlib import Path

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


def test_copy_not_a_directory(temp_directory: Path):
    src_path = temp_directory / "not-exists"
    dest_path = temp_directory / "destination"

    result = runner.invoke(app, ["copy", str(src_path), str(dest_path)])

    assert result.exit_code == 1
