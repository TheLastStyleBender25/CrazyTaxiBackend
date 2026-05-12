from sqlalchemy import  Column, Integer, String, ForeignKey, DateTime
import uuid
from sqlalchemy.dialects.postgresql import UUID
from app.db.session import Base
from datetime import datetime

class Player(Base):
    __tablename__ = "players"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), unique=True, index=True)
    coins = Column(Integer, default=0)
    gems = Column(Integer, default=0)
    level = Column(Integer, default=0)
    xp = Column(Integer, default=0)
    current_city_unlocked = Column(Integer, default=1)
    total_rides_completed = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
