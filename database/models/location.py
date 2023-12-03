from sqlalchemy import Column, Integer, String

from .connection import Base

class Location(Base):
    __tablename__ = 'location'

    id = Column(Integer, primary_key=True)
    title = Column(String)
    address = Column(String)
