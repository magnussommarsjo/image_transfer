from enum import Enum, auto
from pathlib import Path
from typing import Iterator
import shutil
import datetime

import logging

log = logging.getLogger()


def walk(root: str) -> Iterator[Path]:
    """Recureivly iterates through directories and yields file paths"""
    for path in Path(root).iterdir():
        if path.is_dir():
            yield from walk(path)
            continue
        yield path


def _copy_file(source_path: Path, target_path: Path) -> None:
    """Copies file from source to target path"""
    target_path.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source_path, target_path)


def _move_file(source_path: Path, target_path: Path) -> None:
    """Moves file from source to target path"""
    target_path.parent.mkdir(parents=True, exist_ok=True)
    shutil.move(source_path, target_path)


class DateDepth(Enum):
    YEAR = auto()
    MONTH = auto()
    DAY = auto()


def create_path_based_on_creation_date(
    file_path: Path, target_dir: Path, date_depth: DateDepth
) -> Path:
    """Returns path based on creation date of file"""
    timestamp = file_path.stat().st_mtime
    date = datetime.date.fromtimestamp(timestamp)

    match date_depth:
        case DateDepth.YEAR:
            target_path = target_dir.joinpath(str(date.year), file_path.name)
        case DateDepth.MONTH:
            target_path = target_dir.joinpath(
                str(date.year), f"{date.month:02d}", file_path.name
            )
        case DateDepth.DAY:
            target_path = target_dir.joinpath(
                str(date.year), f"{date.month:02d}", f"{date.day:02d}", file_path.name
            )

    return target_path


def copy_files(
    source_dir: Path,
    target_dir: Path,
    date_depth: DateDepth = DateDepth.DAY,
    skip_existing=True,
) -> None:
    """Copies files from source to target directory"""
    for file_path in walk(source_dir):
        target_path = create_path_based_on_creation_date(
            file_path, target_dir, date_depth=date_depth
        )
        if skip_existing and target_path.exists():
            log.info(f"Skipping {file_path}")
            continue
        else:
            log.info(f"Copying {file_path} to {target_path}")
            _copy_file(file_path, target_path)
