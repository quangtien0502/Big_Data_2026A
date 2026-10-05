from sqlalchemy.orm import Session
from app.models.weather import WeatherRecord
from app.schemas.weather import WeatherRecordCreate
from datetime import datetime
from typing import Optional

class WeatherRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, weather_in: WeatherRecordCreate) -> WeatherRecord:
        db_weather = WeatherRecord(**weather_in.model_dump())
        self.db.add(db_weather)
        self.db.commit()
        self.db.refresh(db_weather)
        return db_weather

    def get_multi(
        self,
        skip: int = 0,
        limit: int = 20,
        station_id: Optional[str] = None,
        start_time: Optional[datetime] = None,
        end_time: Optional[datetime] = None
    ):
        query = self.db.query(WeatherRecord)
        if station_id:
            query = query.filter(WeatherRecord.station_id == station_id)
        if start_time:
            query = query.filter(WeatherRecord.timestamp >= start_time)
        if end_time:
            query = query.filter(WeatherRecord.timestamp <= end_time)
        return query.order_by(WeatherRecord.timestamp.desc()).offset(skip).limit(limit).all()

    def count(
        self,
        station_id: Optional[str] = None,
        start_time: Optional[datetime] = None,
        end_time: Optional[datetime] = None
    ) -> int:
        query = self.db.query(WeatherRecord)
        if station_id:
            query = query.filter(WeatherRecord.station_id == station_id)
        if start_time:
            query = query.filter(WeatherRecord.timestamp >= start_time)
        if end_time:
            query = query.filter(WeatherRecord.timestamp <= end_time)
        return query.count()

    def get_by_id(self, id: int) -> WeatherRecord | None:
        return self.db.query(WeatherRecord).filter(WeatherRecord.id == id).first()
