from datetime import datetime
from pathlib import Path
import string
from typing import Iterator, List, Tuple
import shutil

from rich.progress import Progress

import logging
from imgtrf.logger import console
from imgtrf import meta

log = logging.getLogger(__name__)


def copy_files(
    src_dir: Path,
    dest_dir: Path,
    dir_format: str,
    skip_existing=True,
) -> None:
    """Copies files from source to target directory"""
    src_dest_paths = _create_src_dest_pairs(
        src_dir=src_dir,
        dest_dir=dest_dir,
        dir_format=dir_format,
        skip_existing=skip_existing,
    )

    if not src_dest_paths:
        log.info("No files to copy")
        return

    with Progress(console=console) as progress:
        for src_file_path, target_path in progress.track(
            src_dest_paths, description="Copying"
        ):
            log.info(f"Copying {src_file_path} to {target_path}")
            _copy_file(src_file_path, target_path)


def move_files(
    src_dir: Path,
    dest_dir: Path,
    dir_format: str,
    skip_existing=True,
) -> None:
    """Copies files from source to target directory"""
    src_dest_paths = _create_src_dest_pairs(
        src_dir=src_dir,
        dest_dir=dest_dir,
        dir_format=dir_format,
        skip_existing=skip_existing,
    )

    if not src_dest_paths:
        log.info("No files to move")
        return

    with Progress(console=console) as progress:
        for src_file_path, target_path in progress.track(
            src_dest_paths, description="Moving"
        ):
            log.info(f"Moving {src_file_path} to {target_path}")
            _move_file(src_file_path, target_path)


def walk(root: str) -> Iterator[Path]:
    """Recureivly iterates through directories and yields file paths"""
    for path in Path(root).iterdir():
        if path.is_dir():
            yield from walk(path)
            continue
        yield path


def _create_src_dest_pairs(
    src_dir: Path, dest_dir: Path, dir_format: str, skip_existing: bool = True
) -> List[Tuple[str, str]]:
    src_dest_paths: List[Tuple[str, str]] = []

    with Progress(console=console) as progress:
        for src_file_path in progress.track(
            walk(src_dir),
            description="Indexing",
        ):
            target_path = _create_path_by_creation_date(
                src_file_path=src_file_path, dest_dir=dest_dir, dir_format=dir_format
            )
            if skip_existing and target_path.exists():
                log.info(f"Skipping {src_file_path}")
                continue
            else:
                src_dest_paths.append((src_file_path, target_path))
        return src_dest_paths


def _create_path_by_creation_date(
    src_file_path: Path, dest_dir: Path, dir_format: str
) -> Path:
    """Returns path based on creation date of file"""
    date = meta.get_creation_time(src_file_path)
    sub_directories = _create_path_from(date, dir_format)

    return dest_dir / sub_directories / src_file_path.name


def _create_path_from(date_time: datetime, dir_format: str) -> Path:
    """Creates formated path from date_time

    Reference:
        https://docs.python.org/3.8/library/datetime.html#strftime-and-strptime-format-codes

    Args:
        date_time (datetime): time to be used in path formatting
        dir_format (str): String including format codes of how to format the path

    Returns:
        Path: A path formatted by datetime
    """

    # Assume that we strictly indicate format codes with %
    if "%" in dir_format:
        return Path(date_time.strftime(dir_format))

    # If no % signs in dir_format, assume that it is loosly formated and that every
    # character could be a format code.
    path = Path()
    for directory_string in dir_format.split("/"):
        folder_name = ""
        for char in directory_string:
            if char not in string.ascii_letters:
                folder_name += char
                continue
            try:
                dir_part = date_time.strftime(f"%{char}")
            except ValueError:
                # If we cant translate, we append that character instead.
                folder_name += char
            else:
                folder_name += dir_part
        path = path.joinpath(folder_name)

    return path


def _copy_file(src_file_path: Path, dest_path: Path) -> None:
    """Copies file from source to target path"""
    dest_path.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src_file_path, dest_path)


def _move_file(src_file_path: Path, dest_path: Path) -> None:
    """Moves file from source to target path"""
    dest_path.parent.mkdir(parents=True, exist_ok=True)
    shutil.move(src_file_path, dest_path)


def remove_dirs(root_dir: Path) -> None:
    """Recursivly remove empty directories"""
    for path in Path(root_dir).iterdir():
        if path.is_dir():
            remove_dirs(path)

    if Path.cwd() == root_dir.resolve():
        # Cant remove current working directory
        return

    children = [child for child in root_dir.iterdir()]
    # remove if empty
    if len(children) == 0:
        root_dir.rmdir()
        log.info(f"Removed {root_dir}")
