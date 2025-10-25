from pathlib import Path
from constants import BYTES_IN_MB, IMAGES_FOLDER


images_folder_path = list(Path(IMAGES_FOLDER).glob("*.*"))

def get_image_size(images_folder: list) -> None:
    """Get the size of an image in mbytes."""
    for image_path in images_folder:
        size_bytes = image_path.stat().st_size
        size_mb = size_bytes / BYTES_IN_MB

        print(f"Image: {image_path.name}, Size: {size_mb:.2f} MB")


if __name__ == "__main__":
    get_image_size(images_folder_path)
