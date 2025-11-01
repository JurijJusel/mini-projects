from datetime import datetime, timedelta
import calendar
from  rich import print
import requests
from constants import STATION, LAT, LON, DAYS_COUNT, CSV_FILE_PATH
from file import create_csv_file


def get_previous_30_days():
    current_date = datetime.now().date()
    all_dates = [(current_date - timedelta(days=i)).strftime("%Y-%m-%d") for i in range(DAYS_COUNT)]
    return all_dates


def get_meteo_data(station, get_previous_30_days):
    """
    Fetch meteorological data for the previous 30 days.
    Args:
        station (str): Station identifier.
        get_previous_30_days (function): Function that returns a list of date
        strings for the previous 30 days.
    Returns:
        list: A list of dictionaries containing meteorological data for each date.
        [
            {"date": "2025-10-05",
            "observationTimeUtc": "2025-10-05T00:10:00Z",
            "airTemperature": 10.5,
            "feelsLikeTemperature": 9.8,
            "relativeHumidity": 85},
            ...
        ]
    """
    meteo_results = []

    for date_str in get_previous_30_days():
        meteo_url = f"https://api.meteo.lt/v1/stations/{station}/observations/{date_str}"
        resp = requests.get(meteo_url)
        if resp.status_code == 200:
            data = resp.json()
            observations = data.get("observations", [])
            if observations:
                first_obs = observations[0]
                meteo_results.append({
                    "date": date_str,
                    "observationTimeUtc": first_obs.get("observationTimeUtc"),
                    "airTemperature": first_obs.get("airTemperature"),
                    "feelsLikeTemperature": first_obs.get("feelsLikeTemperature"),
                    "relativeHumidity": first_obs.get("relativeHumidity")
                })
    return meteo_results


def get_sun_data(lat, lon, get_previous_30_days):
    """
    Fetch sunrise and sunset times for the previous 30 days.
    Args:
        lat (float): Latitude of the location.
        lon (float): Longitude of the location.
        get_previous_30_days (function): Function that returns a list of
        date strings for the previous 30 days.
    Returns:
        dict: A dictionary with date strings as keys and sunrise/sunset times as values.

        '2025-10-05': {'sunrise': '4:27:26 AM', 'sunset': '3:47:01 PM'},
        '2025-10-04': {'sunrise': '4:25:33 AM', 'sunset': '3:49:31 PM'},
        '2025-10-03': {'sunrise': '4:23:40 AM', 'sunset': '3:52:01 PM'},
        '2025-10-02': {'sunrise': '4:21:47 AM', 'sunset': '3:54:31 PM'}
    """
    sun_results = {}
    for date_str in get_previous_30_days():
        sun_url = f"https://api.sunrise-sunset.org/json?lat={lat}&lng={lon}&date={date_str}&formatted=1"
        resp = requests.get(sun_url)
        if resp.status_code == 200:
            sun_data = resp.json().get("results", {})
            sun_results[date_str] = {
                "sunrise": sun_data.get("sunrise"),
                "sunset": sun_data.get("sunset")
            }
        else:
            sun_results[date_str] = {"sunrise": None, "sunset": None}
    return sun_results


def merge_meteo_sun_data(meteo_data, sun_data):
    merged = []
    for entry in meteo_data:
        date_str = entry["date"]
        entry.update(sun_data.get(date_str, {"sunrise": None, "sunset": None}))
        merged.append(entry)
    return merged


def write_data_to_csv(csv_file, data):
    create_csv_file(csv_file, data)
    print(f"Meteorological and sun data for {len(data)} days have been written to '{csv_file}'.")


if __name__ == "__main__":
    meteo_data = get_meteo_data(STATION, get_previous_30_days)
    sun_data = get_sun_data(LAT, LON, get_previous_30_days)
    merget_data = merge_meteo_sun_data(meteo_data, sun_data)
    print(merget_data)
    #write_data_to_csv(CSV_FILE_PATH, merget_data)
    #for entry in final_data:
    #    print(entry)
