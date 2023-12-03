from sqlalchemy import Column, Integer, String, TIMESTAMP
from sqlalchemy.sql import func

from .connection import Base

class Recipient(Base):
    __tablename__ = 'recipient'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    address = Column(String)
    phone = Column(String)
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())
