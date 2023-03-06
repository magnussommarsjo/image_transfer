from datetime import datetime
from PIL import Image
import piexif

import pytest

from pathlib import Path


def create_image(directory: Path, file_name: str, creation_date: datetime) -> Path:
    """Create dummy image with metadata

    Reference
    ----------
    https://www.cipa.jp/std/documents/e/DC-008-2012_E.pdf

    """
    file_path = directory / file_name
    time_string = (
        f"{creation_date.year}:{creation_date.month:02}:{creation_date.day:02} "
        f"{creation_date.hour:02}:{creation_date.minute:02}:{creation_date.second:02}"
    )

    with Image.new("RGB", (10, 20)) as image:
        exif = {}
        exif.update({"0th": {piexif.ImageIFD.DateTime: time_string}})
        exif.update({"Exif": {piexif.ExifIFD.DateTimeOriginal: time_string}})
        exif.update({"Exif": {piexif.ExifIFD.DateTimeDigitized: time_string}})
        image.save(file_path, exif=piexif.dump(exif))

    return file_path


@pytest.fixture
def temp_image(tmp_path: Path) -> Path:
    image_path = create_image(
        tmp_path, "image.jpg", creation_date=datetime(2020, 1, 1, 12, 00)
    )
    yield image_path


@pytest.fixture
def temp_directory(tmp_path: Path) -> Path:
    # Source for move and copy
    src = tmp_path / "source"
    src_subfolder = src / "subfolder"
    src_subfolder.mkdir(parents=True)

    # Destingation for move and copy
    dest = tmp_path / "destination"
    dest.mkdir()

    # Create files
    create_image(src, "file01.jpg", datetime(2020, 1, 1, 12, 00))
    create_image(src_subfolder, "file02.jpg", datetime(2020, 2, 1, 12, 00))

    yield tmp_path
