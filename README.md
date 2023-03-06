# Image Transfer

Basic package to transfer images and videos into a date structure.

This package looks through both images and videos for creation time metadata.
If found it can copy or move the files from a source directory to a destination directory.
The sub directory of the destination directory will be based on creation time. As default
year/month/day e.g 2023/01/27.

## Usage

Copy from one directory to another

```pwsh
imgtrf copy {source/directory} {destination/directory}
```

Move from one directory to another

```pwsh
imgtrf move {source/directory} {destination/directory}
```

Change format of destination directory structure.  
Defaults to `Y/m/d` for Year/Month/Day. Directories are seperated by `/` and the format codes can be found [here](./docs/format_codes.md).

```pwsh
imgtrf copy --dir-format {dir_format} {source/directory} {destination/directory}
```

You can also remove empty directories.

```pwsh
imgtrf remove dirs {target/root/directory}
```

You can always find specific help with the `--help` flag.

```pwsh
# Either for the application
imgtrf --help

# Or for a specific command
imgtrf copy --help
```

## Installation

Installation of image-transfer is simply done via a pip command.

```pwsh
pip install image-transfer
```

### FFmpeg

To support gathering metadata from video files, you need to have **FFmpeg** installed and added to your PATH environment variable. FFmpeg can either be installed from their site [ffmpeg.org](https://ffmpeg.org/download.html)  
It can also be donwloaded via winget in windows or apt in linux.

```pwsh
winget install --id Gyan.FFmpeg
```

or if on linux

```bash
sudo apt install ffmpeg
```

Make sure to check your environment variables. Some times even a restart of your computer is necessary for them to be read in properly.
