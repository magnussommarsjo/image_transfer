from pathlib import Path
from typing import Dict, Optional

from imgtrf import meta
from unittest.mock import patch
import pytest
from datetime import datetime


def test_get_image_meta(temp_image: Path):
    metadata = meta.get_image_meta(temp_image)
    assert len(metadata) != 0
    assert "DateTime" in metadata.keys()


@pytest.mark.parametrize(
    "mock_meta,expected",
    [
        (
            {
                "not_a_date": "12345",
                "not_a_date_2": "abcdef",
            },
            None,
        ),
        (
            {
                "DateTime": "2023:01:01 12:00:00",
                "not_a_date_2": "abcdef",
            },
            datetime(2023, 1, 1, 12, 0, 0),
        ),
    ],
)
def test_get_image_creation_time(mock_meta: Dict, expected: Optional[datetime]):
    with patch("imgtrf.meta.get_image_meta", return_value=mock_meta):
        creation_time = meta.get_image_creation_time('path/should/not/matter')

    assert creation_time == expected
