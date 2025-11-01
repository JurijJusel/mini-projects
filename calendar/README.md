# Calendar Meteorological Data Fetcher

This project fetches meteorological data from api.meteo.lt and
sunrise/sunset from api.sunrise-sunset.org
for a specified location over the past 30 days.
The combined data is then saved into a CSV file for further analysis.


## Features

- Fetches daily meteorological data from Meteo.lt for a specified weather station.
- Retrieves sunrise and sunset times for a given latitude and longitude.
- Merges the meteorological and sun data into a unified format.
- Saves the combined data into a CSV file.


## Requirements

- Python 3.8+
- Requests library
- Pydantic library
- Pandas library


## Install dependencies:

```bash
pip install -r requirements.txt
```

- if use uv:
```bash
uv pip install -r pyproject.toml
```


## Run  the script:

```bash
python3 main.py
```


## Usage
1. Configure the constants in `constants.py` to set the weather station,
    latitude, longitude, number of days to fetch, and output CSV file path.
2. Run the script using Python.
3. The output CSV file will contain the merged meteorological and sun data f
    or the specified period.
    [
    {
        'date': '2025-11-01',
        'observationTimeUtc': '2025-11-01 00:00:00',
        'airTemperature': 7.6,
        'feelsLikeTemperature': 5.7,
        'relativeHumidity': 97,
        'sunrise': '5:20:11 AM',
        'sunset': '2:44:43 PM',
        'day_length': '09:24:32'
    },
    {
        'date': '2025-10-31',
        'observationTimeUtc': '2025-10-31 00:00:00',
        'airTemperature': 7.4,
        'feelsLikeTemperature': 4.1,
        'relativeHumidity': 97,
        'sunrise': '5:18:11 AM',
        'sunset': '2:46:47 PM',
        'day_length': '09:28:36'
    }
    ...
    ]

## License
This project is licensed under the MIT License.
