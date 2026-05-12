from  sqlalchemy import Column, Integer, ForeignKey
from app.db.session import Base
import uuid
from sqlalchemy.dialects.postgresql import UUID

class PlayerClaimedMilestone(Base):
    __tablename__ = 'player_claimed_milestones'
    id = Column(Integer, primary_key=True, index=True)
    player_id = Column(UUID(as_uuid= True), ForeignKey('players.id'), nullable=False, index=True)
    milestone_id = Column(Integer, ForeignKey('ride_milestones.id'), nullable=False, index=True)