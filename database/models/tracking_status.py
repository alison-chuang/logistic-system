from sqlalchemy import Column, Integer, String, TIMESTAMP, ForeignKey
from sqlalchemy.sql import func

from .connection import Base

class TrackingStatus(Base):
    __tablename__ = 'tracking_status'

    id = Column(Integer, primary_key=True)
    order_sno = Column(Integer, ForeignKey('order.sno'), nullable=False)
    tracking_status = Column(String)
    location_id = Column(Integer, ForeignKey('location.id'), nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now(), nullable=False)
