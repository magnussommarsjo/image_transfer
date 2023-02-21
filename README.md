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



# Installation

Installation is done by cloning the repository to to your computer and do a local install with pip
```sh
git clone https://github.com/magnussommarsjo/transfer_by_date.git
cd {your/cloned/repository}
pip install .
```

To support gathering metadata from videos you need to have **FFmpeg** installed and added to your PATH environment variable. FFmpeg can either be installed from their site [ffmpeg.org](https://ffmpeg.org/download.html) or via winget
```sh
winget install --id Gyan.FFmpeg
```
Make sure to check your environment variables. Some times even a restart of your computer is necessary for them to be read in properly. 