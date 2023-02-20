from pprint import pprint
from pathlib import Path
import ffmpeg
from PIL import Image
from PIL.ExifTags import TAGS


def get_image_meta(path: str) -> dict[str, str]:
    """Get image metadata from file"""
    image = Image.open(path)
    exif = {}
    for tag, value in image.getexif().items():
        if tag in TAGS.keys():
            exif |= {TAGS[tag]: value}
        else:
            exif |= {tag: value}

    return exif

def get_movie_meta(path: str) -> dict[str, str]:
    """Get movie metadata from file"""
    try:
        meta = ffmpeg.probe(path)
    except FileNotFoundError as e:
        raise ImportError( # ToDo: Not really an import error...
            "Could not use ffmpeg propperly. Make sure its installed correctly and added to path"
        ) from e
    return meta



if __name__ == "__main__":
    # pprint(TAGS)
    # pprint(get_image_meta('./tmp/image.JPG'))

    pprint()
    path = Path("./tmp/movie.MP4").resolve()
    print(path.exists())
