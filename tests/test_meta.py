from pathlib import Path

from imgtrf import meta


def test_get_image_meta(temp_directory: Path):
    file = temp_directory / "source" / "file01.jpg"
    metadata = meta.get_image_meta(file)
    assert len(metadata) != 0
    assert "DateTime" in metadata.keys()
