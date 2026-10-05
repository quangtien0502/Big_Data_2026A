from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class WeatherRecordBase(BaseModel):
    station_id: str
    timestamp: datetime
    temperature: Optional[float] = None
    rainfall: Optional[float] = Field(None, ge=0)
    weather_condition: Optional[str] = None
    latitude: Optional[float] = Field(None, ge=-90, le=90)
    longitude: Optional[float] = Field(None, ge=-180, le=180)
    source: Optional[str] = None

class WeatherRecordCreate(WeatherRecordBase):
    pass

class WeatherRecordResponse(WeatherRecordBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True
