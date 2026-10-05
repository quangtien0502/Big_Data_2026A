from sqlalchemy.orm import Session
from app.models.traffic import TrafficRecord
from app.schemas.traffic import TrafficRecordCreate
from datetime import datetime
from typing import Optional

class TrafficRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, traffic_in: TrafficRecordCreate) -> TrafficRecord:
        db_traffic = TrafficRecord(**traffic_in.model_dump())
        self.db.add(db_traffic)
        self.db.commit()
        self.db.refresh(db_traffic)
        return db_traffic

    def get_multi(
        self,
        skip: int = 0,
        limit: int = 20,
        road_id: Optional[str] = None,
        start_time: Optional[datetime] = None,
        end_time: Optional[datetime] = None
    ):
        query = self.db.query(TrafficRecord)
        if road_id:
            query = query.filter(TrafficRecord.road_id == road_id)
        if start_time:
            query = query.filter(TrafficRecord.timestamp >= start_time)
        if end_time:
            query = query.filter(TrafficRecord.timestamp <= end_time)
        return query.order_by(TrafficRecord.timestamp.desc()).offset(skip).limit(limit).all()

    def count(
        self,
        road_id: Optional[str] = None,
        start_time: Optional[datetime] = None,
        end_time: Optional[datetime] = None
    ) -> int:
        query = self.db.query(TrafficRecord)
        if road_id:
            query = query.filter(TrafficRecord.road_id == road_id)
        if start_time:
            query = query.filter(TrafficRecord.timestamp >= start_time)
        if end_time:
            query = query.filter(TrafficRecord.timestamp <= end_time)
        return query.count()

    def get_by_id(self, id: int) -> TrafficRecord | None:
        return self.db.query(TrafficRecord).filter(TrafficRecord.id == id).first()
