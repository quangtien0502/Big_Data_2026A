from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class TrafficRecordBase(BaseModel):
    road_id: str
    timestamp: datetime
    vehicle_count: int = Field(..., ge=0)
    avg_speed: float = Field(..., ge=0)
    source: Optional[str] = None

class TrafficRecordCreate(TrafficRecordBase):
    pass

class TrafficRecordResponse(TrafficRecordBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True
