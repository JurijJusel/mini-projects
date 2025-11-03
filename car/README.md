# MKAuto Image Scraper

This Python script scrapes all car listings and their images from [mkauto.lt](https://www.mkauto.lt),
automatically saving all vehicle images to a local folder.


## ⚙️ Features

- Collects all car detail page URLs across multiple pages
- Extracts all image links from each car page
- Downloads and saves all images locally
- Automatically names files based on image IDs
- Includes error handling and polite scraping delay


## Requirements

- Python 3.8+
- Requests library
- beautifulsoup4
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
