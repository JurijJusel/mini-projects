from pydantic import BaseModel

class ImageInfo(BaseModel):

    image_name: str
    resolution_size: str
    size_mb: float
