from pathlib import Path
import json


def create_data_json_file(data: list[dict], json_file_path: str):
    """
    Saves a list of dictionaries to a JSON file, overwriting any existing file.
    Args:
        data (list[dict]): List of dictionaries to save.
        json_file_path (str): Path to the JSON file.
    Returns:
        str: Message confirming where the data was saved.
    """
    path = Path(json_file_path)
    path.parent.mkdir(parents=True, exist_ok=True)

    with open(path, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=2, ensure_ascii=False)

    return f" JSON data saved to '{json_file_path}'"


def open_json_file(json_file_path: str):
    """
    Opens a JSON file and returns its contents as a Python object.
    Args:
        json_file_path (str): Path to the JSON file to open.
    Returns:
        The parsed JSON content (usually a list or dict), or None if the file
        does not exist or contains invalid JSON.
    Notes:
        - The function safely handles missing files.
        - The function safely handles invalid JSON and returns None in that case.
        - The file is opened in read-only mode; it will not modify the JSON file.
    """
    path = Path(json_file_path)

    if not path.is_file():
        print(f"JSON file not found: {json_file_path}")
        return None

    try:
        with open(path, "r", encoding="utf-8") as file:
            data = json.load(file)
        return data
    except json.JSONDecodeError:
        print(f"Invalid JSON format in '{json_file_path}'")
        return None
