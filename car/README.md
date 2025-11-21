# MKAuto Image Scraper

This Python script scrapes all car listings and their images from [mkauto.lt]
(https://www.mkauto.lt), automatically saving all vehicle images
to a local folder, analyzes and sorts images into color-based folders.


## Features

- Collects all car detail page URLs across multiple pages
- Extracts all image links from each car page
- Downloads and saves all images locally
- Automatically names files based on image IDs
- Includes error handling and polite scraping delay


# Image Color Analyzer
- After downloading, the script can:
- Read each image
- Detect dominant colors (Red, Green, Blue, Gray, etc.)
- Automatically sort images into folders:
- mkauto_images/red/
- mkauto_images/green/
- mkauto_images/blue/
- mkauto_images/gray/
- Missing folders are created automatically.

# About IMAGES_FOLDER_FOR_PROCESSING

Processing all downloaded images about (≈1000 photos)
is very slow and may take up to 3 hours because each image must be:
- loaded into memory
- converted to RGB
- scanned pixel-by-pixel
- compared with each color palette

To avoid long processing time while developing or testing, the script uses:

IMAGES_FOLDER_FOR_PROCESSING = "mkauto_images/test"

✔ Why this is important
You can put only a few test images inside mkauto_images/test/
Run the sorting script faster (usually a few seconds)
Confirm detection logic works correctly
Avoid waiting hours every time during development
✔ When you're ready for full sorting
Change the folder to your real full image directory:

IMAGES_FOLDER_FOR_PROCESSING = "mkauto_images"


## Requirements

- Python 3.8+
- Requests library
- beautifulsoup4
- Pillow
- rich
- Internet connection


## Install dependencies:

```bash
pip install -r requirements.txt
```

- if use uv:
```bash
uv pip install -r pyproject.toml
```


## Run  the script:

```bash
python3 main.py
```

## Run the color-sorting script

```bash
python3 image_sort.py
```
