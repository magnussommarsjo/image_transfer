from pathlib import Path

import typer
from rich import print

from imgtrf import logger
from imgtrf import core

app = typer.Typer(name="Image Transfer", add_completion=False)


_option_dir_format = typer.Option(
    default="Y/m/d",
    help="""Format of destination directory.Directories seperated with '/' and format codes with '%' followed by single character.""",
)


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
    dir_format: str = "Y/m/d",
):
    """Copy files from source dir to destination dir"""

    source_path = Path(src_dir).resolve()
    destination_path = Path(dest_dir).resolve()

    if not source_path.exists() or not source_path.is_dir():
        print("Source directory does not exists")
        raise NotADirectoryError(src_dir)

    core.copy_files(
        src_dir=source_path, dest_dir=destination_path, dir_format=dir_format
    )


@app.command()
def move(
    src_dir: str,
    dest_dir: str,
    dir_format: str = _option_dir_format,
):
    """Move files from source dir to destination dir"""

    source_path = Path(src_dir).resolve()
    destination_path = Path(dest_dir).resolve()

    if not source_path.exists() or not source_path.is_dir():
        print("Source directory does not exists")
        raise NotADirectoryError(src_dir)

    core.move_files(
        src_dir=source_path, dest_dir=destination_path, dir_format=dir_format
    )


remove_app = typer.Typer(name="remove")
app.add_typer(remove_app)


@remove_app.callback()
def remove_main():
    """Removal of directories and files"""
    pass


@remove_app.command("dirs")
def remove_dirs(directory: str = typer.Argument(..., help="Root directory to remove")):
    """Remove empty directories recursivly, target directory included"""
    dir_path = Path(directory)

    if not dir_path.exists() or not dir_path.is_dir():
        print("Directory does not exists")
        raise NotADirectoryError(dir_path)

    core.remove_dirs(dir_path)
