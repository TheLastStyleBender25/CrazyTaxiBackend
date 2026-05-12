from sqlalchemy.dialects.postgresql import UUID
import uuid
from sqlalchemy import DateTime, Column, Integer, String, DateTime, ForeignKey
from app.db.session import Base
from datetime import datetime

class AvailableTaxi(Base):
    __tablename__ = 'available_taxis'

    id = Column(Integer, primary_key=True, index=True)
    taxi_type = Column(String, nullable=False)
    price = Column(Integer, nullable=False)
    fuel = Column(Integer, default=100)
    fuel_cost_per_km = Column(Integer, default=1)
    health = Column(Integer, default=100)
    base_fare_price = Column(Integer, default=0)
    health_cost_per_km = Column(Integer, default=1)
    created_at = Column(DateTime, default=datetime.now())