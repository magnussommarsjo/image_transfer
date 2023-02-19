import typer
from imgtrf.core import copy_files
from pathlib import Path

app = typer.Typer()


@app.command()
def copy(src_dir: str, dest_dir: str):
    """Copy files from source dir to destination dir"""

    source_path = Path(src_dir).resolve()
    destination_path = Path(dest_dir).resolve()

    if not source_path.exists() or not source_path.is_dir():
        print("Source directory does not exists")
        raise NotADirectoryError(src_dir)

    print("Copying files...")
    copy_files(src_dir=source_path, dest_dir=destination_path)
    print("...finished copying files")

@app.command()
def move(src_dir: str, dest_dir: str):
    """Move files from source dir to destination dir"""
    print("Moving files")


app()
