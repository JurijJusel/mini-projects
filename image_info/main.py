import PIL
from PIL import Image
from pathlib import Path
from constants import BYTES_IN_MB, IMAGES_FOLDER
from rich import print
from model import ImageInfo, RGB
import numpy as np


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
        with Image.open(str(image_path)) as img:
            width, height = img.size
            resolution = str(width) + "x" + str(height)

            rgb_data = count_rgb_pixels(img)

        size_bytes = image_path.stat().st_size
        size_mb = round(size_bytes / BYTES_IN_MB, 3)

        data = {
            "image_name": image_path.name,
            "resolution_size": resolution,
            "rgb": RGB(**rgb_data),
            "size_mb": size_mb,
        }
        item = ImageInfo(**data)
        results.append(item.model_dump())

    return results


def count_rgb_pixels(img) -> dict:
    """
        Count how many pixels in an image are predominantly Red, Green, or Blue,
    and calculate their percentage of total area.
    Args:
        img (PIL.Image): The image to analyze.
    Returns:
        dict: A dictionary with counts and percentages of red, green, and blue pixels.
    """
    image = img.convert("RGB")
    np_image = np.array(image)

    red_channel = np_image[:, :, 0]
    green_channel = np_image[:, :, 1]
    blue_channel = np_image[:, :, 2]

    red_mask = (red_channel > green_channel) & (red_channel > blue_channel)
    green_mask = (green_channel > red_channel) & (green_channel > blue_channel)
    blue_mask = (blue_channel > red_channel) & (blue_channel > green_channel)

    red_count = int(np.sum(red_mask))
    green_count = int(np.sum(green_mask))
    blue_count = int(np.sum(blue_mask))

    total_pixels = np_image.shape[0] * np_image.shape[1]

    red_percent = round((red_count / total_pixels) * 100, 2)
    green_percent = round((green_count / total_pixels) * 100, 2)
    blue_percent = round((blue_count / total_pixels) * 100, 2)

    rgb_data = {
        "red": {
            "pixels": red_count,
            "area_percent": red_percent
        },
        "green": {
            "pixels": green_count,
            "area_percent": green_percent
        },
        "blue": {
            "pixels": blue_count,
            "area_percent": blue_percent
        }
    }

    return rgb_data


def print_results(results: list) -> None:
    """Print the results in a formatted way."""
    for item in results:
        print(item)


if __name__ == "__main__":
    results = get_image_size(images_folder_path)
    print_results(results)
