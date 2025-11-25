from __future__ import annotations
from pydantic import BaseModel, Field
from typing import List


class SkelbiuAutoModel(BaseModel):
    Item_ID: str = Field(..., alias='Item_ID')
    Title: str
    City: str
    Creation_date: str = Field(..., alias='Creation date')
    Item_Params: List[str] = Field(..., alias='Item Params')
    Price: str
    Link: str
    Image_URL: str = Field(..., alias='Image URL')
