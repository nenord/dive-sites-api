from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, Float

from app.database import Base

class Site_db(Base):
    __tablename__ = "sites"

    id = Column(Integer, primary_key=True)
    name = Column(String(32))
    slug = Column(String(32), unique=True)
    lat = Column(Float)
    lon = Column(Float)
    description = Column(String(1024))
