from pathlib import Path
from datetime import datetime
import platform

import ffmpeg
from PIL import Image
from PIL.ExifTags import TAGS
import PIL

import logging
from imgtrf.logger import log_func
from imgtrf import exceptions

from typing import Optional

log = logging.getLogger(__name__)


# Supported formats
IMAGE_EXT = {"jpg", "jpeg" "png"}
VIDEO_EXT = {"mp4"}


def get_creation_time(path: Path) -> Optional[datetime]:
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
    creation_time: datetime = None

    if _is_image(path):
        creation_time = get_image_creation_time(path)

    if _is_video(path):
        creation_time = get_video_creation_time(path)

    if _is_windows() and creation_time is None:
        creation_time = get_win_creation_time(path)

    # TODO: Return None or raise error?
    # if not creation_time:
    #   raise Error()?!
    return creation_time


@log_func(log)
def get_image_creation_time(path: Path) -> Optional[datetime]:
    """Returns creation time if exists in image metadata"""
    try:
        metadata = get_image_meta(path)
    except PIL.UnidentifiedImageError as e:
        log.error(e)
        return None

    time_format = r"%Y:%m:%d %H:%M:%S"
    time_string = metadata.get("DateTime")
    creation_time = datetime.strptime(time_string, time_format)

    return creation_time


@log_func(log)
def get_video_creation_time(path: Path) -> Optional[datetime]:
    try:
        metadata = get_video_meta(path)
    except exceptions.MetaDataError as e:
        log.error(e)
        return None

    # Look at 'creation_time' in 'format'
    time_string = metadata.get("format", {}).get("tags", {}).get("creation_time", None)
    if time_string is not None:
        return _string_to_datetime(time_string)

    # Look at 'creation_time' in streams/tags
    streams: list[dict] = metadata.get("streams", [])
    if streams:
        # TODO: streams consists of both video and audio. Loop through?
        time_string = streams[0].get("tags", {}).get("creation_time")
        if time_string is not None:
            return _string_to_datetime(time_string)

def _string_to_datetime(time_string: str) -> datetime:
    # Since vefore python 3.11 datetime.fromitoformat cant handle timezones.
    if len(time_string) > 19:
        time_string = time_string[:19]
    return datetime.fromisoformat(time_string)


@log_func(log)
def get_win_creation_time(path: Path) -> datetime:
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
            exif.update({TAGS[tag]: value})
        else:
            exif.update({tag: value})

    return exif


def get_video_meta(path: Path) -> dict:
    """Get video metadata from file using ffmpeg"""
    try:
        meta = ffmpeg.probe(path)
    except FileNotFoundError as e:
        raise exceptions.MetaDataError(  # ToDo: Not really an import error...
            "Could not use ffmpeg propperly. Make sure its installed correctly and added to path"
        ) from e
    except ffmpeg.Error as e:
        raise exceptions.MetaDataError(
            f"Could not retrive meta data from file: {path}"
        ) from e

    return meta


def _is_windows() -> bool:
    return platform.system() == "Windows"


def _is_image(path: Path) -> bool:
    ext = path.suffix.lower()[1:]
    return ext in IMAGE_EXT


def _is_video(path: Path) -> bool:
    ext = path.suffix.lower()[1:]
    return ext in VIDEO_EXT
