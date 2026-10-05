from sqlalchemy import Column, Integer, String, Float, DateTime, func, ForeignKey, Index
from sqlalchemy.orm import relationship
from app.models.base import Base

class TrafficRecord(Base):
    __tablename__ = "traffic_records"

    id = Column(Integer, primary_key=True, index=True)
    road_id = Column(String, ForeignKey("roads.road_id"), nullable=False, index=True)
    timestamp = Column(DateTime(timezone=True), nullable=False, index=True)
    vehicle_count = Column(Integer, nullable=False)
    avg_speed = Column(Float, nullable=False)
    source = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    road = relationship("Road", back_populates="traffic_records")

    __table_args__ = (
        Index("ix_traffic_records_road_id_timestamp", "road_id", "timestamp"),
    )
