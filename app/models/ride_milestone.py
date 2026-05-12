from sqlalchemy import Column, Integer, String
from app.db.session import Base

class RideMilestone(Base):
    __tablename__ = 'ride_milestones'

    id = Column(Integer, primary_key=True, index=True)
    required_rides = Column(Integer, nullable=False)
    gem_reward = Column(Integer, nullable=False)