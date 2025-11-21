import math
from PIL import Image
from pathlib import Path
from constants import IMAGES_FOLDER_FOR_PROCESSING, PALETTES, THRESHOLD, COLOR_FOLDERS
from rich import print
from rich.progress import track
from file import ensure_folder_exists


def color_distance(c1, c2):
    """
    Euclidean distance between two RGB colors.
    Args:
        c1 (tuple): RGB color 1.
        c2 (tuple): RGB color 2.
    Returns:
        float: Distance value.
    """
    return math.sqrt(sum((a - b) ** 2 for a, b in zip(c1, c2)))


def get_image_all_pixels(img_path):
    """
    Load all pixels from an image.
    Args:
        img_path (str or Path): Path to the image.
    Returns:
        list[tuple]: List of RGB pixel values.
    """
    with Image.open(img_path) as img:
        img = img.convert("RGB")
        pixels = list(img.getdata())
    return pixels


def count_color_pixels(img_pixels, palette, threshold):
    """
    Count how many pixels are red in an image.
    Args:
        img_path: Path to image
        palette: List of red RGB tuples
        threshold: Max distance to consider a pixel red

    Returns:
        int: number of red pixels
        float: percentage of red pixels
    """
    color_count = 0

    for pixel in img_pixels:
        for color in palette:
            if color_distance(pixel, color) < threshold:
                color_count += 1
                break

    return color_count


def get_dominant_color(img_pixels, palettes, threshold):
    """
    Determine which palette color dominates the image.
    Args:
        img_pixels (list[tuple]): Pixel data.
        palettes (dict[str, list]): Color palettes.
        threshold (float): Pixel distance threshold.
    Returns:
        str: Dominant palette name.
    """
    counts = {}
    for name, palette in palettes.items():
        counts[name] = count_color_pixels(img_pixels, palette, threshold)

    dominant_color = max(counts, key=counts.get)
    return dominant_color


def save_image_to_folder(img_path, save_folder_path):
    """
    Save an image to a folder. Creates the folder if it does not exist.
    Args:
        img_path (str or Path): Path to the source image.
        save_folder_path (str or Path): Folder where the image will be saved.
    Returns:
        Path: Full path to the saved image.
    """
    img_path = Path(img_path)
    save_folder = Path(save_folder_path)
    save_path = save_folder / img_path.name

    with Image.open(img_path) as img:
        img.save(save_path)

    print(f"Image saved to: {save_path}")
    return save_path


def main_image_sort():
    """
    Sort images by dominant color and save them in designated folders.
    """
    input_folder = ensure_folder_exists(IMAGES_FOLDER_FOR_PROCESSING)
    img_folder_for_process = list(input_folder.glob("*.*"))
    for index, img_path in track(
        enumerate(img_folder_for_process, start=1),
        description="Check and save car images ...",
        total=len(img_folder_for_process)):

        pixels = get_image_all_pixels(img_path)
        out_dominant_palette = get_dominant_color(pixels, PALETTES, THRESHOLD)

        folder_path = COLOR_FOLDERS.get(out_dominant_palette)
        if folder_path:
            folder = ensure_folder_exists(folder_path)
            save_image_to_folder(img_path, folder)


if __name__ == "__main__":
    main_image_sort()
