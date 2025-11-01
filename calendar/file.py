import pandas as pd
from pathlib import Path


def create_csv_file(csv_file_path: str, data: list):
    """
    function creates or appends data to a CSV file from a list of dictionaries.
    Args:
        csv_file_path (str): Path to the CSV file.
        data (list): Data to be written to the CSV file.
                if data:dict pd.DataFrame([data], index=[0])
    Returns:
        str: confirmation message indicating for operation
    """
    df = pd.DataFrame(data)
    file_path = Path(csv_file_path)
    try:
        if file_path.exists():
            df.to_csv(file_path, index=False, mode="w", header=True)
            return f"The data is added to the '{file_path}' file."
        else:
            file_path.parent.mkdir(parents=True, exist_ok=True)
            df.to_csv(file_path, index=False, mode="w", header=True)
            return f"created '{file_path}' file and data written to it"

    except Exception as e:
            raise Exception(f"An error occurred while writing data to CSV file '{file_path}': {e}")


def read_csv_file(csv_file_path: str) -> str:
    """
    function read data from csv file
    Args:
        csv_file_path: (str) path to csv file
    Returns:
        pandas.DataFrame: DataFrame containing the data read from the CSV file
        Returns None if file does not exist or cannot be read
    """
    try:
        df = pd.read_csv(csv_file_path)
        return df
    except FileNotFoundError:
        print(f"Error: csv file '{csv_file_path}' does not exist.")
        return None
    except pd.errors.ParserError as e:
        print(f"Error reading csv file '{csv_file_path}' error: {e}")
        return None
