from sqlalchemy.orm import Session
from app.models.road import Road
from app.schemas.road import RoadCreate

class RoadRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_road_id(self, road_id: str) -> Road | None:
        return self.db.query(Road).filter(Road.road_id == road_id).first()

    def create(self, road_in: RoadCreate) -> Road:
        db_road = Road(**road_in.model_dump())
        self.db.add(db_road)
        self.db.commit()
        self.db.refresh(db_road)
        return db_road

    def get_multi(self, skip: int = 0, limit: int = 20):
        return self.db.query(Road).offset(skip).limit(limit).all()

    def count(self) -> int:
        return self.db.query(Road).count()
