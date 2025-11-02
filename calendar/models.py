from typing import Optional
from pydantic import BaseModel
from datetime import datetime


class MeteoData(BaseModel):
    date: str
    observationTimeUtc: datetime
    airTemperature: float
    feelsLikeTemperature: float
    relativeHumidity: int
    sunrise: Optional[datetime] = None
    sunset: Optional[datetime] = None
    day_length: Optional[str] = None
