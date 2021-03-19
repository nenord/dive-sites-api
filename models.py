from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, Float

from database import Base

class Sitedb(Base):
    __tablename__ = "sites"

    id = Column(Integer, primary_key=True)
    name = Column(String(32))
    slug = Column(String(32), unique=True)
    lat = Column(Float)
    lon = Column(Float)
    description = Column(String(1024))
    depth = Column(Integer)
    park_approach = Column(String(512))

    def __repr__(self):
       return "<Site(name='{}', slug='{}', depth={}, lat={}, lon={})>"\
                .format(self.name, self.slug, self.depth, self.lat, self.lon)
