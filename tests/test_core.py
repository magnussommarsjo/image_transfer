from pathlib import Path

from imgtrf import core


def test_copy_files(temp_directory: Path):
    src_path = temp_directory / "source"
    dest_path = temp_directory / "destination"

    core.copy_files(src_path, dest_path)

    assert (
        temp_directory / "destination" / "2020" / "01" / "01" / "file01.jpg"
    ).exists()
