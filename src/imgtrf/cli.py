from pathlib import Path
import logging

import typer
from rich import print

from imgtrf.logger import root_logger
from imgtrf.core import copy_files, move_files, DateDepth

# Set up logging
log = logging.getLogger(__name__)
root_logger.addHandler(logging.StreamHandler())

app = typer.Typer()


def parse_date_depth(date_depth: str) -> DateDepth:
    match date_depth.lower():
        case "day":
            return DateDepth.DAY
        case "month":
            return DateDepth.MONTH
        case "year":
            return DateDepth.YEAR
        case _:
            raise ValueError(f"Argument {date_depth=} not recognised")


@app.command()
def copy(
    src_dir: str,
    dest_dir: str,
    date_level: str = "day",
):
    """Copy files from source dir to destination dir"""

    date_depth = parse_date_depth(date_level)

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

    date_depth = parse_date_depth(date_level)

    source_path = Path(src_dir).resolve()
    destination_path = Path(dest_dir).resolve()

    if not source_path.exists() or not source_path.is_dir():
        print("Source directory does not exists")
        raise NotADirectoryError(src_dir)

    move_files(src_dir=source_path, dest_dir=destination_path, date_depth=date_depth)


@app.callback()
def main(verbose: bool = False, debug: bool = False):
    if verbose:
        root_logger.setLevel(logging.INFO)

    if debug:
        root_logger.setLevel(logging.DEBUG)
