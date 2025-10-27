from pydantic import BaseModel


class Red(BaseModel):
    pixels: int
    area_percent: float

class Green(BaseModel):
    pixels: int
    area_percent: float

class Blue(BaseModel):
    pixels: int
    area_percent: float

class RGB(BaseModel):
    red: Red
    green: Green
    blue: Blue

class ImageInfo(BaseModel):
    image_name: str
    resolution_size: str
    rgb: RGB
    size_mb: float
