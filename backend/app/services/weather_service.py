from sqlalchemy.orm import Session
from app.repositories.weather_repository import WeatherRepository
from app.schemas.weather import WeatherRecordCreate
from fastapi import HTTPException
from datetime import datetime
from typing import Optional

class WeatherService:
    def __init__(self, db: Session):
        self.repository = WeatherRepository(db)

    def create_weather_record(self, weather_in: WeatherRecordCreate):
        return self.repository.create(weather_in)

    def get_weather_records(
        self,
        page: int = 1,
        page_size: int = 20,
        station_id: Optional[str] = None,
        start_time: Optional[datetime] = None,
        end_time: Optional[datetime] = None
    ):
        skip = (page - 1) * page_size
        items = self.repository.get_multi(
            skip=skip,
            limit=page_size,
            station_id=station_id,
            start_time=start_time,
            end_time=end_time
        )
        total = self.repository.count(station_id=station_id, start_time=start_time, end_time=end_time)
        return items, total

    def get_weather_record(self, record_id: int):
        record = self.repository.get_by_id(record_id)
        if not record:
            raise HTTPException(status_code=404, detail="Weather record not found")
        return record
