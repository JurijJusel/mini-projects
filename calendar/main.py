import requests
from datetime import datetime, timedelta
from typing import  List, Dict
from constants import BASE_METEO_URL, BASE_SUN_URL, DAYS_COUNT, CSV_FILE_PATH
from models import MeteoData
from file import create_csv_file
from rich import print


def get_previous_days(days_count: int) -> List[str]:
    """
    Generate a list of date strings for the previous 'days_count' days.
    Args:
        days_count (int): Number of previous days to generate dates.
        from constants import DAYS_COUNT
        can be changed to the desired number of days
    Returns:
        List[str]: List of date strings in 'YYYY-MM-DD' format.
        [
            '2025-11-01',
            '2025-10-31',
            '2025-10-30',
            '2025-10-29',
            '2025-10-28',
            '2025-10-27'
        ]
    """
    current_date = datetime.now().date()
    all_dates = [(current_date - timedelta(days=i)).strftime("%Y-%m-%d") for i in range(days_count)]

    return all_dates


def get_meteo_data(base_url: str,  previous_days: list[str]) -> List[Dict]:
    """
    Fetch Meteo.lt data for the past 30 days (first hourly record each day)
    Args:
        base_url (str): Base URL for the Meteo.lt API from constants
        previous_days (list[str]): List of date strings for the previous days
    Returns:
        List[Dict]: List of dictionaries containing meteorological data
    outputs:
        [
            {
                'date': '2025-11-01',
                'observationTimeUtc': '2025-11-01 00:00:00',
                'airTemperature': 7.6,
                'feelsLikeTemperature': 5.7,
                'relativeHumidity': 97
            },
            {
                'date': '2025-10-31',
                'observationTimeUtc': '2025-10-31 00:00:00',
                'airTemperature': 7.4,
                'feelsLikeTemperature': 4.1,
                'relativeHumidity': 97
            }
        ]
    """
    meteo_data = []

    for date_str in previous_days:
        url = f"{base_url}/observations/{date_str}"
        print(url)
        resp = requests.get(url)
        if resp.status_code != 200:
            continue

        data = resp.json()
        obs = data.get("observations")
        if not obs:
            continue

        obs_number = obs[0]
        meteo_data.append({
            "date": date_str,
            "observationTimeUtc": obs_number["observationTimeUtc"],
            "airTemperature": obs_number["airTemperature"],
            "feelsLikeTemperature": obs_number["feelsLikeTemperature"],
            "relativeHumidity": obs_number["relativeHumidity"],
        })

    return meteo_data


def get_sun_data(base_url: str, previous_days: list[str]) -> Dict[str, Dict]:
    """
    Fetch sunrise/sunset times for past 30 days.
    Args:
        base_url (str): Base URL for the Sunrise-Sunset API from constants
        previous_days (list[str]): List of date strings for the previous days
    Returns:
        Dict[str, Dict]: Dictionary with date strings as keys and
        sunrise, sunset, day_length times as values
    outputs:
    {
        '2025-11-01': {
            'sunrise': '2025-11-01T05:20:11+00:00',
            'sunset': '2025-11-01T14:44:43+00:00',
            'day_length': '9:24:32'
        },
        '2025-10-31': {
            'sunrise': '2025-10-31T05:18:11+00:00',
            'sunset': '2025-10-31T14:46:47+00:00',
            'day_length': '9:28:36'
        }
    }
    """
    sun_results = {}
    for date_str in previous_days:
        url = f"{base_url}&date={date_str}&formatted=0"
        print(url)
        resp = requests.get(url)
        if resp.status_code != 200:
            continue

        data = resp.json().get("results", {})
        if not data:
            continue

        sun_results[date_str] = {
            "sunrise": data.get("sunrise"),
            "sunset": data.get("sunset"),
            "day_length": str(timedelta(seconds=data.get("day_length", 0)))
        }

    return sun_results


def merge_meteo_sun(meteo_data: List[Dict], sun_data: Dict[str, Dict]) -> List[MeteoData]:
    """
    Combine weather and sun data into MeteoData objects.
    Args:
        meteo_data (List[Dict]): List of meteorological data dictionaries
        sun_data (Dict[str, Dict]): Dictionary of sun data with date strings as keys
    Returns:
        List[MeteoData]: List of merged MeteoData objects
    outputs:
        [
            MeteoData(
                date='2025-11-01',
                observationTimeUtc=datetime.datetime(2025, 11, 1, 0, 0),
                airTemperature=7.6,
                feelsLikeTemperature=5.7,
                relativeHumidity=97,
                sunrise=datetime.datetime(2025, 11, 1, 5, 20, 11, tzinfo=TzInfo(0)),
                sunset=datetime.datetime(2025, 11, 1, 14, 44, 43, tzinfo=TzInfo(0)),
                day_length='9:24:32'
            ),
            MeteoData(
                date='2025-10-31',
                observationTimeUtc=datetime.datetime(2025, 10, 31, 0, 0),
                airTemperature=7.4,
                feelsLikeTemperature=4.1,
                relativeHumidity=97,
                sunrise=datetime.datetime(2025, 10, 31, 5, 18, 11, tzinfo=TzInfo(0)),
                sunset=datetime.datetime(2025, 10, 31, 14, 46, 47, tzinfo=TzInfo(0)),
                day_length='9:28:36'
            ),
            ...
        ]
    """
    merged = []
    for record in meteo_data:
        date = record["date"]
        sun = sun_data.get(date, {})
        merged.append(MeteoData(**record, **sun))

    return merged


def save_to_csv(data: List[MeteoData], csv_path: str):
    """
    Save merged data to CSV.
    Args:
        data (List[MeteoData]): List of MeteoData objects to save
        csv_path (str): Path to the CSV file
    outputs data to csv file:
        [
            {
            'date': '2025-10-29',
            'observationTimeUtc': datetime.datetime(2025, 10, 29, 0, 0),
            'airTemperature': 6.3,
            'feelsLikeTemperature': 4.3,
            'relativeHumidity': 97,
            'sunrise': datetime.datetime(2025, 10, 29, 5, 14, 11, tzinfo=TzInfo(0)),
            'sunset': datetime.datetime(2025, 10, 29, 14, 50, 58, tzinfo=TzInfo(0)),
            'day_length': '9:36:47'
            },
            {
            'date': '2025-10-28',
            'observationTimeUtc': datetime.datetime(2025, 10, 28, 0, 0),
            'airTemperature': 4.1,
            'feelsLikeTemperature': 2.1,
            'relativeHumidity': 95,
            'sunrise': datetime.datetime(2025, 10, 28, 5, 12, 11, tzinfo=TzInfo(0)),
            'sunset': datetime.datetime(2025, 10, 28, 14, 53, 6, tzinfo=TzInfo(0)),
            'day_length': '9:40:55'
            },
            ...
        ]
    """
    data = [record.model_dump() for record in data]

    create_csv_file(csv_path, data)
    print(f"Meteorological and sun data for {len(data)} days have been written to '{csv_path}'.")


def main():
    print("Getting previous days dates ...")
    previous_30_days = get_previous_days(DAYS_COUNT)

    print("Fetching Meteo.lt data ...")
    meteo_data = get_meteo_data(BASE_METEO_URL, previous_30_days)

    print("Fetching Sunrise/Sunset data ...")
    sun_data = get_sun_data(BASE_SUN_URL, previous_30_days)

    print("Merging datasets ...")
    merged = merge_meteo_sun(meteo_data, sun_data)

    print("Saving to CSV ...")
    save_to_csv(merged, CSV_FILE_PATH)


if __name__ == "__main__":
    main()
