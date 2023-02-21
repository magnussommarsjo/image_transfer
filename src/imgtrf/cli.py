import typer
from imgtrf.core import copy_files, move_files, DateDepth
from pathlib import Path
import logging

from rich import print

from imgtrf.logger import root_logger as log

# Set up logging
stream_handler = logging.StreamHandler()
log.addHandler(stream_handler)

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
    verbose: bool = False,
    debug: bool = False,
):
    """Copy files from source dir to destination dir"""

    date_depth = parse_date_depth(date_level)

    source_path = Path(src_dir).resolve()
    destination_path = Path(dest_dir).resolve()

    _set_log_level(verbose, debug)

    if not source_path.exists() or not source_path.is_dir():
        print("Source directory does not exists")
        raise NotADirectoryError(src_dir)

    copy_files(src_dir=source_path, dest_dir=destination_path, date_depth=date_depth)


@app.command()
def move(
    src_dir: str,
    dest_dir: str,
    date_level: str = "day",
    verbose: bool = False,
    debug: bool = False,
):
    """Move files from source dir to destination dir"""

    date_depth = parse_date_depth(date_level)

    source_path = Path(src_dir).resolve()
    destination_path = Path(dest_dir).resolve()

    _set_log_level(verbose, debug)

    if not source_path.exists() or not source_path.is_dir():
        print("Source directory does not exists")
        raise NotADirectoryError(src_dir)

    move_files(src_dir=source_path, dest_dir=destination_path, date_depth=date_depth)


def _set_log_level(verbose: bool = False, debug: bool = False):
    if verbose:
        log.setLevel(logging.INFO)

    if debug:
        log.setLevel(logging.DEBUG)
