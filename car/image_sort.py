import math
from PIL import Image
from pathlib import Path
from constants import IMAGES_FOLDER, PALETTES, THRESHOLD, COLOR_FOLDERS
from rich import print
from rich.progress import track


images_folder_path = list(Path(IMAGES_FOLDER).glob("*.*"))


def color_distance(c1, c2):
    """Euclidean distance between two RGB colors."""
    return math.sqrt(sum((a - b) ** 2 for a, b in zip(c1, c2)))


def get_image_all_pixels(img_path):
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
    counts = {}
    for name, palette in palettes.items():
        counts[name] = count_color_pixels(img_pixels, palette, threshold)

    dominant_color = max(counts, key=counts.get)
    return dominant_color


def create_folder(path):
    folder = Path(path)
    if folder.exists():
        return str(folder)
    else:
        folder.mkdir(parents=True, exist_ok=True)
        print(f"Folder created: '{folder}'")
        return str(folder)


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


if __name__ == "__main__":
    for index, img_path in track(
        enumerate(images_folder_path, start=1),
        description="Check and save car images ...",
        total=len(images_folder_path)):

        pixels = get_image_all_pixels(img_path)
        out_dominant_palette = get_dominant_color(pixels, PALETTES, THRESHOLD)

        folder_path = COLOR_FOLDERS.get(out_dominant_palette)
        if folder_path:
            folder = create_folder(folder_path)
            save_image_to_folder(img_path, folder)
