from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime
from app.db.session import Base
from sqlalchemy.dialects.postgresql import UUID
import uuid
from datetime import datetime

class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(UUID(as_uuid=True), default=uuid.uuid4, primary_key=True)
    player_id = Column(UUID(as_uuid=True), ForeignKey("players.id"), nullable=False)
    amount = Column(Integer, nullable=False)
    transaction_type = Column(String, nullable=False)
    reason = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.now())