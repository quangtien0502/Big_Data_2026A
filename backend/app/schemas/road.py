from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class RoadBase(BaseModel):
    road_id: str = Field(..., description="Unique ID for the road")
    road_name: Optional[str] = None
    district: Optional[str] = None
    latitude: Optional[float] = Field(None, ge=-90, le=90)
    longitude: Optional[float] = Field(None, ge=-180, le=180)

class RoadCreate(RoadBase):
    pass

class RoadResponse(RoadBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True
