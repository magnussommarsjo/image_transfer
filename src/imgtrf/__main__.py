import typer
from imgtrf.core import copy_files
from pathlib import Path

app = typer.Typer()


@app.command()
def copy(source: str, destination: str):
    """Copy files from source dir to destination dir"""

    source_path = Path(source).resolve()
    destination_path = Path(destination).resolve()

    if not source_path.exists() or not source_path.is_dir():
        print("Source directory does not exists")
        raise NotADirectoryError(source)

    print("Copying files...")
    copy_files(source_dir=source_path, target_dir=destination_path)
    print("...finished copying files")

@app.command()
def move(source: str, destination: str):
    """Move files from source dir to destination dir"""
    print("Moving files")


app()
