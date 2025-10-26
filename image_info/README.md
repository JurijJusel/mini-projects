# Image Info Extractor

    A Python project to extract image information (filename, resolution, and file size)
from a folder of images.
    Uses `PIL` (Pillow) for image processing, `pathlib` for file handling,
and `rich` for pretty printing.

---

## 🛠️ Features

- Extracts image resolution (WIDTHxHEIGHT)
- Extracts image file size in megabytes\
- Evaluates pixel color distribution (Red, Green, Blue) and percentage area
- Outputs structured results as dictionaries
- Pretty-prints results using Rich

---

##  Requirements

- Python 3.11 or higher

---

## Installation
## Install dependencies:

```bash
pip install -r requirements.txt
```

- if use uv:
```bash
uv pip install -r pyproject.toml
```
---

## Run  the script:

```bash
python3 main.py
```

## Example Output
{
    'image_name': 'Screenshot 2025-02-11 at 18.39.59.png',
    'resolution_size': '1427x722',
    'rgb': {
        'red': {'pixels': 28961, 'area_percent': 2.81},
        'green': {'pixels': 60703, 'area_percent': 5.89},
        'blue': {'pixels': 25812, 'area_percent': 2.51}
    },
    'size_mb': 0.199
}

---

## License
This project is licensed under the MIT License.
You are free to use, modify, and distribute this script.
