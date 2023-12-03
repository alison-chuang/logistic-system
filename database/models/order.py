from sqlalchemy import Column, Integer, TIMESTAMP, ForeignKey
from sqlalchemy.sql import func

from .connection import Base

class Order(Base):
    __tablename__ = 'order'

    sno = Column(Integer, primary_key=True)
    recipient_id = Column(Integer, ForeignKey('recipient.id'))
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())
