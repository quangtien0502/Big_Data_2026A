from sqlalchemy.orm import Session
from app.repositories.traffic_repository import TrafficRepository
from app.repositories.road_repository import RoadRepository
from app.schemas.traffic import TrafficRecordCreate
from fastapi import HTTPException
from datetime import datetime
from typing import Optional

class TrafficService:
    def __init__(self, db: Session):
        self.repository = TrafficRepository(db)
        self.road_repo = RoadRepository(db)

    def create_traffic_record(self, traffic_in: TrafficRecordCreate):
        road = self.road_repo.get_by_road_id(traffic_in.road_id)
        if not road:
            raise HTTPException(status_code=400, detail=f"Road {traffic_in.road_id} not found")
        return self.repository.create(traffic_in)

    def get_traffic_records(
        self,
        page: int = 1,
        page_size: int = 20,
        road_id: Optional[str] = None,
        start_time: Optional[datetime] = None,
        end_time: Optional[datetime] = None
    ):
        skip = (page - 1) * page_size
        items = self.repository.get_multi(
            skip=skip,
            limit=page_size,
            road_id=road_id,
            start_time=start_time,
            end_time=end_time
        )
        total = self.repository.count(road_id=road_id, start_time=start_time, end_time=end_time)
        return items, total

    def get_traffic_record(self, record_id: int):
        record = self.repository.get_by_id(record_id)
        if not record:
            raise HTTPException(status_code=404, detail="Traffic record not found")
        return record
