from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean
from sqlalchemy.dialects.postgresql import UUID
from app.db.session import Base
from datetime import datetime
import uuid

class OwnedTaxi(Base):
    __tablename__ = "owned_taxis"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    player_id = Column(UUID(as_uuid=True), ForeignKey("players.id"), nullable=False, index=True)
    taxi_id = Column(Integer, ForeignKey("available_taxis.id"), nullable=False)
    taxi_type = Column(String, nullable=False)
    fuel = Column(Integer, default=100)
    fuel_cost_per_km = Column(Integer, default=1)
    health = Column(Integer, default=100)
    health_cost_per_km = Column(Integer, default=1)
    is_active = Column(Boolean, default=False)
    base_fare_price = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.now())
    updated_at = Column(DateTime, default=datetime.now(), onupdate=datetime.now())
