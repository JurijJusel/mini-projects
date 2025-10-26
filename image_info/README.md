# Image Info Extractor

    A Python project to extract image information (filename, resolution, and file size)
from a folder of images.
    Uses `PIL` (Pillow) for image processing, `pathlib` for file handling,
and `rich` for pretty printing.

---

## 🛠️ Features

- Extracts image resolution (WIDTHxHEIGHT)
- Extracts image file size in megabytes
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

{'image_name': 'Screenshot 2024-07-22 at 00.08.49.png', 'resolution_size': '1393x757', 'size_mb': 0.289}

---

## License
This project is licensed under the MIT License.
You are free to use, modify, and distribute this script.
