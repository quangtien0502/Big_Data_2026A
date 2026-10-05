from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.weather import WeatherRecordCreate, WeatherRecordResponse
from app.schemas.common import PaginatedResponse
from app.services.weather_service import WeatherService
from datetime import datetime
from typing import Optional

router = APIRouter()

@router.post("/", response_model=WeatherRecordResponse)
def create_weather(weather_in: WeatherRecordCreate, db: Session = Depends(get_db)):
    service = WeatherService(db)
    return service.create_weather_record(weather_in)

@router.get("/", response_model=PaginatedResponse[WeatherRecordResponse])
def get_weather_records(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    station_id: Optional[str] = None,
    start_time: Optional[datetime] = None,
    end_time: Optional[datetime] = None,
    db: Session = Depends(get_db)
):
    service = WeatherService(db)
    items, total = service.get_weather_records(page, page_size, station_id, start_time, end_time)
    return {"items": items, "page": page, "page_size": page_size, "total": total}

@router.get("/{id}", response_model=WeatherRecordResponse)
def get_weather_record(id: int, db: Session = Depends(get_db)):
    service = WeatherService(db)
    return service.get_weather_record(id)

@router.get("/station/{station_id}", response_model=PaginatedResponse[WeatherRecordResponse])
def get_weather_by_station(
    station_id: str,
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db)
):
    service = WeatherService(db)
    items, total = service.get_weather_records(page=page, page_size=page_size, station_id=station_id)
    return {"items": items, "page": page, "page_size": page_size, "total": total}
