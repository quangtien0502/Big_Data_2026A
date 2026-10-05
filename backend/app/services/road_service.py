from sqlalchemy.orm import Session
from app.repositories.road_repository import RoadRepository
from app.schemas.road import RoadCreate
from fastapi import HTTPException

class RoadService:
    def __init__(self, db: Session):
        self.repository = RoadRepository(db)

    def create_road(self, road_in: RoadCreate):
        existing_road = self.repository.get_by_road_id(road_in.road_id)
        if existing_road:
            raise HTTPException(status_code=400, detail=f"Road {road_in.road_id} already exists")
        return self.repository.create(road_in)

    def get_roads(self, page: int = 1, page_size: int = 20):
        skip = (page - 1) * page_size
        items = self.repository.get_multi(skip=skip, limit=page_size)
        total = self.repository.count()
        return items, total

    def get_road(self, road_id: str):
        road = self.repository.get_by_road_id(road_id)
        if not road:
            raise HTTPException(status_code=404, detail=f"Road {road_id} not found")
        return road
