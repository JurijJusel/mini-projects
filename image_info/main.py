import PIL
from PIL import Image
from pathlib import Path
from constants import BYTES_IN_MB, IMAGES_FOLDER
from rich import print
from model import ImageInfo

images_folder_path = list(Path(IMAGES_FOLDER).glob("*.*"))

def get_image_size(images_folder: list) -> list:
    """
    Extract image information from a list of image file paths.
    Args:
        images_folder (List[Path]): A list of image file paths to process.
    Returns:
        List[Dict[str, str, float]]:
            A list of dictionaries where each dictionary contains:
                - "image_name" (str): The filename of the image.
                - "resolution_size" (str): The image resolution in "WIDTHxHEIGHT" format.
                - "size_mb" (float): The image file size in megabytes (rounded to 3 decimals).
    """
    results = []

    for image_path in images_folder:
        with PIL.Image.open(str(image_path)) as img:
            width, height = img.size
            resolution = str(width) + "x" + str(height)

        size_bytes = image_path.stat().st_size
        size_mb = round(size_bytes / BYTES_IN_MB, 3)

        data = {
            "image_name": image_path.name,
            "resolution_size": resolution,
            "size_mb": size_mb,
        }
        item = ImageInfo(**data)
        results.append(item.model_dump())

    return results


def print_results(results: list) -> None:
    """Print the results in a formatted way."""
    for item in results:
        print(item)


if __name__ == "__main__":
    results = get_image_size(images_folder_path)
    print_results(results)
