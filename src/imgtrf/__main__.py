import typer
from imgtrf.core import copy_files, move_files
from pathlib import Path
import logging

log = logging.getLogger()

app = typer.Typer()


@app.command()
def copy(src_dir: str, dest_dir: str, verbose: bool = False):
    """Copy files from source dir to destination dir"""

    source_path = Path(src_dir).resolve()
    destination_path = Path(dest_dir).resolve()

    if verbose:
        log.setLevel("INFO")

    if not source_path.exists() or not source_path.is_dir():
        print("Source directory does not exists")
        raise NotADirectoryError(src_dir)

    copy_files(src_dir=source_path, dest_dir=destination_path)


@app.command()
def move(src_dir: str, dest_dir: str, verbose: bool = False):
    """Move files from source dir to destination dir"""

    source_path = Path(src_dir).resolve()
    destination_path = Path(dest_dir).resolve()

    if verbose:
        log.setLevel("INFO")

    if not source_path.exists() or not source_path.is_dir():
        print("Source directory does not exists")
        raise NotADirectoryError(src_dir)

    move_files(src_dir=source_path, dest_dir=destination_path)


app()
