from app.db.session import Base
import uuid
from sqlalchemy import Column, String, DateTime, Boolean, Integer, ForeignKey
from  sqlalchemy.dialects.postgresql import UUID
from datetime import datetime

class OrgUser(Base):
    __tablename__ = "org_users"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), unique=True)
    password = Column(String, nullable=False)