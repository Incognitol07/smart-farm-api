# app/schemas/sensor.py

from pydantic import BaseModel
from typing import Optional

class SensorCreate(BaseModel):
    type: str
    location: Optional[str] = None
    min_value: Optional[float] = None
    max_value: Optional[float] = None


class SensorReading(BaseModel):
    value: float