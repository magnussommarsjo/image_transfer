from pathlib import Path
from datetime import datetime
import platform

import ffmpeg
from PIL import Image
from PIL.ExifTags import TAGS

import logging
from imgtrf.logger import log_func, root_logger as log


# Supported formats
IMAGE_EXT = ("jpg", "jpeg" "png")
VIDEO_EXT = "mp4"


def get_creation_time(path: Path) -> datetime | None:
    """Returns file creation date

    --- STRATEGY ---
    1) Figure out format of file.
    2) Try to extract creation time metadata from that file
    3) If no metadata can be gathered try to fallback on win creation time.
    3) No metadata for file: Skip file and write error log


    Args:
        path (Path): Path to file

    Returns:
        datetime | None: file creation time
    """
    ext = path.suffix.lower()[1:]
    creation_time: datetime = None

    if ext in IMAGE_EXT:
        creation_time = get_image_creation_time(path)

    if ext in VIDEO_EXT:
        creation_time = get_video_creation_time(path)

    if isWindows() and creation_time is None:
        creation_time = get_win_creation_time(path)

    # TODO: Return None or raise error?
    # if not creation_time:
    #   raise Error()?!
    return creation_time


@log_func()
def get_image_creation_time(path: Path) -> datetime | None:
    """Returns creation time if exists in image metadata"""
    metadata = get_image_meta(path)
    time_format = r"%Y:%m:%d %H:%M:%S"
    time_string = metadata.get("DateTime")
    creation_time = datetime.strptime(time_string, time_format)
    return creation_time


@log_func()
def get_video_creation_time(path: Path) -> datetime | None:
    metadata = get_video_meta(path)

    # Look at 'creation_time' in 'format'
    creation_time: datetime = None
    time_string = metadata.get("format", {}).get("tags", {}).get("creation_time", None)
    if time_string is not None:
        return datetime.fromisoformat(time_string)

    # Look at 'creation_time' in streams/tags
    streams: list[dict] = metadata.get("streams", [])
    if streams:
        # TODO: streams consists of both video and audio. Loop through?
        time_string = streams[0].get("tags", {}).get("creation_time")
        if time_string is not None:
            return datetime.fromisoformat(time_string)


@log_func()
def get_win_creation_time(path: Path):
    """Get creation time from windows file

    This does not wotk in linux environment since linuc does not store creation time.
    """
    timestamp = path.stat().st_mtime
    return datetime.fromtimestamp(timestamp)


def get_image_meta(path: Path) -> dict:
    """Get image metadata from file using pillow"""
    image = Image.open(path)
    exif = {}
    for tag, value in image.getexif().items():
        if tag in TAGS.keys():
            exif |= {TAGS[tag]: value}
        else:
            exif |= {tag: value}

    return exif


def get_video_meta(path: Path) -> dict:
    """Get video metadata from file using ffmpeg"""
    try:
        meta = ffmpeg.probe(path)
    except FileNotFoundError as e:
        raise ImportError(  # ToDo: Not really an import error...
            "Could not use ffmpeg propperly. Make sure its installed correctly and added to path"
        ) from e
    return meta


def isWindows():
    return platform.system() == "Windows"


if __name__ == "__main__":
    # Bsic logging
    log.setLevel(logging.DEBUG)
    stream_handler = logging.StreamHandler()
    log.addHandler(stream_handler)

    from rich.pretty import pprint

    # pprint(TAGS)
    # pprint(get_image_meta("./tmp/image.JPG"))

    pprint(get_video_meta(Path("./tmp/video.MP4")))

    pprint(get_creation_time(Path("./tmp/video.MP4")))

    pprint(get_creation_time(Path("./tmp/image.JPG")))
