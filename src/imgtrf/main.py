from pathlib import Path
from src.imgtrf.core import copy_files, DateDepth

import logging

logging.basicConfig(level=logging.INFO)

# source_dir = Path(r"C:\Users\magnu\Desktop\100CANON")
# target_dir = Path(r"U:\Kamera")

# From backup photo in synology into seperate folders
source_dir = Path(r"U:\Magnus\DCIM\Camera")
target_dir = Path(r"U:\Magnus")


assert source_dir.exists()
copy_files(source_dir, target_dir, date_depth=DateDepth.MONTH)
print("FINISHED")
