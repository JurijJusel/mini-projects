from typing import Optional
from pydantic import BaseModel


class MeteoData(BaseModel):
    date: str
    observationTimeUtc: str
    airTemperature: float
    feelsLikeTemperature: float
    relativeHumidity: int
    sunrise: Optional[str] = None
    sunset: Optional[str] = None
    day_length: Optional[str] = None
