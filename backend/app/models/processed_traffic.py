from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, func, Index
from app.models.base import Base

class ProcessedTrafficRecord(Base):
    __tablename__ = "processed_traffic_records"

    id = Column(Integer, primary_key=True, index=True)
    road_id = Column(String, nullable=False, index=True)
    timestamp = Column(DateTime(timezone=True), nullable=False, index=True)
    district = Column(String, nullable=True, index=True)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    vehicle_count = Column(Integer, nullable=True)
    avg_speed = Column(Float, nullable=True)
    temperature = Column(Float, nullable=True)
    rainfall = Column(Float, nullable=True)
    anomaly_score = Column(Float, nullable=True)
    is_anomaly = Column(Boolean, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
