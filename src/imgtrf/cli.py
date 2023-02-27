from pathlib import Path

import typer
from rich import print

from imgtrf import logger
from imgtrf.core import copy_files, move_files, DateDepth

app = typer.Typer(name="Image Transfer", add_completion=False)


@app.callback()
def main(verbose: bool = False, debug: bool = False):
    """Image Transfer

    Used to transfer images and video files from a directory
    into a new directory with date folder structure.
    """
    # Set verbosity
    logger.set_verbosity(verbose, debug)


@app.command()
def copy(
    src_dir: str,
    dest_dir: str,
    date_level: str = "day",
):
    """Copy files from source dir to destination dir"""

    date_depth = _parse_date_depth(date_level)

    source_path = Path(src_dir).resolve()
    destination_path = Path(dest_dir).resolve()

    if not source_path.exists() or not source_path.is_dir():
        print("Source directory does not exists")
        raise NotADirectoryError(src_dir)

    copy_files(src_dir=source_path, dest_dir=destination_path, date_depth=date_depth)


@app.command()
def move(
    src_dir: str,
    dest_dir: str,
    date_level: str = "day",
):
    """Move files from source dir to destination dir"""

    date_depth = _parse_date_depth(date_level)

    source_path = Path(src_dir).resolve()
    destination_path = Path(dest_dir).resolve()

    if not source_path.exists() or not source_path.is_dir():
        print("Source directory does not exists")
        raise NotADirectoryError(src_dir)

    move_files(src_dir=source_path, dest_dir=destination_path, date_depth=date_depth)


def _parse_date_depth(date_depth: str) -> DateDepth:
    """Parses string to DateDepth

    Args:
        date_depth (str): Depth as 'day' | 'month' | 'year'

    Raises:
        ValueError: If not argument matches

    Returns:
        DateDepth: Date depth as enum
    """
    if date_depth.lower() == "day":
        return DateDepth.DAY
    if date_depth.lower() == "month":
        return DateDepth.MONTH
    if date_depth.lower() == "year":
        return DateDepth.YEAR

    raise ValueError(f"Argument {date_depth=} not recognised")
