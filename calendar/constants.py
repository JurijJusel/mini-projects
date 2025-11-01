
# Meteo.lt station for Vilnius
STATION = "vilniaus-ams"
BASE_METEO_URL = f"https://api.meteo.lt/v1/stations/{STATION}"


# Latitude and Longitude for Vilnius
LAT, LON = 54.6872, 25.2797
BASE_SUN_URL = f"https://api.sunrise-sunset.org/json?lat={LAT}&lng={LON}"


DAYS_COUNT = 30


CSV_FILE_PATH = "data/meteo_data.csv"
