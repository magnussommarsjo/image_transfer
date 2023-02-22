# Image Transfer

Basic package to transfer images and videos into a date structure.

This package looks through both images and videos for creation time metadata.
If found it can copy or move the files from a source directory to a destination directory
where it will create a new folder structure following below format.
> **YYYY / MM / DD**  
>  
> **YYYY**: Year as in '2023'  
> **MM**: Month as in '01' for January  
> **DD**: Day as in '02' for second day in the month  

# Usage

Copy from one directory to another
```
imgtrf copy {source/directory} {destination/directory}
```

Move from one directory to another
```
imgtrf move {source/directory} {destination/directory}
```

Change 'depth' of destination folder structure
```
imgtrf copy --date-level=month {source/directory} {destination/directory}
```


# Installation

Installation is done via PyPI
```sh
pip install image-transfer
```

To support gathering metadata from videos you need to have **FFmpeg** installed and added to your PATH environment variable. FFmpeg can either be installed from their site [ffmpeg.org](https://ffmpeg.org/download.html) or via winget
```
winget install --id Gyan.FFmpeg
```
or if on linux
```sh
sudo apt install ffmpeg
```
Make sure to check your environment variables. Some times even a restart of your computer is necessary for them to be read in properly. 