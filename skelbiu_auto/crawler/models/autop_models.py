from __future__ import annotations
from pydantic import BaseModel
from typing import List, Dict, Optional


class AutopliusCarParameters(BaseModel):
    First_Registration: str
    Mileage: str
    Engine: str
    Fuel: str
    Body_Type: str
    Doors: str
    Drive: str
    Gearbox: str
    Climate_Control: str
    Color: str
    Tech_Inspection: str
    Rim_Size: str
    Weight: str
    Seats: str
    Euro_Standard: str
    CO2_Emission: str
    Pollution_Tax: str
    City_Consumption: Optional[str]
    Highway_Consumption: Optional[str]
    Average_Consumption: Optional[str]

class AutopliusCarDescription(BaseModel):
    Description: List[str]

class AutopliusCarFeatures(BaseModel):
    Features: Dict

class AutopliusCarModel(BaseModel):
    Id: str
    Price: str
    Phone: str
    Title: str
    Link: str
    Parameters: AutopliusCarParameters
    Description: AutopliusCarDescription
    Features: AutopliusCarFeatures
