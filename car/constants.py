
BASE_URL = "https://www.mkauto.lt"


OUTPUT_DIR = "mkauto_images"


JSON_FILE_PATH = "data/cars_data.json"


IMAGES_FOLDER_FOR_PROCESSING = "mkauto_images/test"


BYTES_IN_MB = 1024 * 1024  # 1 MB = 1,048,576 bytes


THRESHOLD = 60


GREEN_PALETTE = [
    (0, 100, 0),     # dark green
    (34, 139, 34),   # forest green
    (0, 128, 0),     # green
]


BLUE_PALETTE = [
    (0, 0, 128),  # navy
    (0, 0, 255),  # blue
    (0, 0, 205),  # medium blue
]


RED_PALETTE = [
    (178, 34, 34),   # firebrick
    (220, 20, 60),   # crimson
    (139, 0, 0),     # dark red
]


PALETTES = {
    "GREEN_PALETTE": GREEN_PALETTE,
    "BLUE_PALETTE": BLUE_PALETTE,
    "RED_PALETTE": RED_PALETTE
}


COLOR_FOLDERS = {
    "BLUE_PALETTE": "mkauto_images/blue",
    "GREEN_PALETTE": "mkauto_images/green",
    "RED_PALETTE": "mkauto_images/red"
}

