from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.traffic import TrafficRecordCreate, TrafficRecordResponse
from app.schemas.common import PaginatedResponse
from app.services.traffic_service import TrafficService
from datetime import datetime
from typing import Optional

router = APIRouter()

@router.post("/", response_model=TrafficRecordResponse)
def create_traffic(traffic_in: TrafficRecordCreate, db: Session = Depends(get_db)):
    service = TrafficService(db)
    return service.create_traffic_record(traffic_in)

@router.get("/", response_model=PaginatedResponse[TrafficRecordResponse])
def get_traffic_records(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    road_id: Optional[str] = None,
    start_time: Optional[datetime] = None,
    end_time: Optional[datetime] = None,
    db: Session = Depends(get_db)
):
    service = TrafficService(db)
    items, total = service.get_traffic_records(page, page_size, road_id, start_time, end_time)
    return {"items": items, "page": page, "page_size": page_size, "total": total}

@router.get("/{id}", response_model=TrafficRecordResponse)
def get_traffic_record(id: int, db: Session = Depends(get_db)):
    service = TrafficService(db)
    return service.get_traffic_record(id)

@router.get("/road/{road_id}", response_model=PaginatedResponse[TrafficRecordResponse])
def get_traffic_by_road(
    road_id: str,
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db)
):
    service = TrafficService(db)
    items, total = service.get_traffic_records(page=page, page_size=page_size, road_id=road_id)
    return {"items": items, "page": page, "page_size": page_size, "total": total}
