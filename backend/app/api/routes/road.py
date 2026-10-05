from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.road import RoadCreate, RoadResponse
from app.schemas.common import PaginatedResponse
from app.schemas.traffic import TrafficRecordResponse
from app.services.road_service import RoadService
from app.services.traffic_service import TrafficService

router = APIRouter()

@router.post("/", response_model=RoadResponse)
def create_road(road_in: RoadCreate, db: Session = Depends(get_db)):
    service = RoadService(db)
    return service.create_road(road_in)

@router.get("/", response_model=PaginatedResponse[RoadResponse])
def get_roads(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db)
):
    service = RoadService(db)
    items, total = service.get_roads(page, page_size)
    return {"items": items, "page": page, "page_size": page_size, "total": total}

@router.get("/{road_id}", response_model=RoadResponse)
def get_road(road_id: str, db: Session = Depends(get_db)):
    service = RoadService(db)
    return service.get_road(road_id)

@router.get("/{road_id}/traffic", response_model=PaginatedResponse[TrafficRecordResponse])
def get_road_traffic(
    road_id: str,
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db)
):
    service = TrafficService(db)
    items, total = service.get_traffic_records(page=page, page_size=page_size, road_id=road_id)
    return {"items": items, "page": page, "page_size": page_size, "total": total}
