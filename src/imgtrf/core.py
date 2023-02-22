from enum import Enum, auto
from pathlib import Path
from typing import Iterator
import shutil

from rich import progress

import logging
from imgtrf import meta

log = logging.getLogger(__name__)


def walk(root: str) -> Iterator[Path]:
    """Recureivly iterates through directories and yields file paths"""
    for path in Path(root).iterdir():
        if path.is_dir():
            yield from walk(path)
            continue
        yield path


class DateDepth(Enum):
    YEAR = auto()
    MONTH = auto()
    DAY = auto()


def create_path_based_on_creation_date(
    src_file_path: Path, dest_dir: Path, date_depth: DateDepth
) -> Path:
    """Returns path based on creation date of file"""
    date = meta.get_creation_time(src_file_path)

    match date_depth:
        case DateDepth.YEAR:
            target_path = dest_dir.joinpath(str(date.year), src_file_path.name)
        case DateDepth.MONTH:
            target_path = dest_dir.joinpath(
                str(date.year), f"{date.month:02d}", src_file_path.name
            )
        case DateDepth.DAY:
            target_path = dest_dir.joinpath(
                str(date.year),
                f"{date.month:02d}",
                f"{date.day:02d}",
                src_file_path.name,
            )

    return target_path


def copy_files(
    src_dir: Path,
    dest_dir: Path,
    date_depth: DateDepth = DateDepth.DAY,
    skip_existing=True,
) -> None:
    """Copies files from source to target directory"""
    src_dest_paths = _create_src_dest_pairs(
        src_dir, dest_dir, date_depth, skip_existing
    )

    if not src_dest_paths:
        log.info("No files to copy")
        return

    for src_file_path, target_path in progress.track(
        src_dest_paths, description="Copying files"
    ):
        log.info(f"Copying {src_file_path} to {target_path}")
        _copy_file(src_file_path, target_path)


def move_files(
    src_dir: Path,
    dest_dir: Path,
    date_depth: DateDepth = DateDepth.DAY,
    skip_existing=True,
) -> None:
    """Copies files from source to target directory"""
    src_dest_paths = _create_src_dest_pairs(
        src_dir, dest_dir, date_depth, skip_existing
    )

    if not src_dest_paths:
        log.info("No files to move")
        return

    for src_file_path, target_path in progress.track(
        src_dest_paths, description="Moving files"
    ):
        log.info(f"Moving {src_file_path} to {target_path}")
        _move_file(src_file_path, target_path)


def _create_src_dest_pairs(
    src_dir: Path, dest_dir: Path, date_depth: DateDepth, skip_existing: bool = True
) -> list[tuple[str, str]]:
    src_dest_paths: list[tuple[str, str]] = []
    for src_file_path in walk(src_dir):
        target_path = create_path_based_on_creation_date(
            src_file_path, dest_dir, date_depth=date_depth
        )
        if skip_existing and target_path.exists():
            log.info(f"Skipping {src_file_path}")
            continue
        else:
            src_dest_paths.append((src_file_path, target_path))
    return src_dest_paths


def _copy_file(src_file_path: Path, dest_path: Path) -> None:
    """Copies file from source to target path"""
    dest_path.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src_file_path, dest_path)


def _move_file(src_file_path: Path, dest_path: Path) -> None:
    """Moves file from source to target path"""
    dest_path.parent.mkdir(parents=True, exist_ok=True)
    shutil.move(src_file_path, dest_path)
