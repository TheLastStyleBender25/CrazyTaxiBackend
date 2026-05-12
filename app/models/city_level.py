from sqlalchemy import Column
from sqlalchemy import Integer
from app.db.session import Base

class CityLevel(Base):
    __tablename__ = "city_levels"

    id = Column(Integer, primary_key=True, index=True)
    level = Column(Integer, nullable=False, unique=True)
    gems_required = Column(Integer, nullable=False)