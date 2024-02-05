from sqlalchemy import Column, Integer, DateTime, Float, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from config.db import Base


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    total = Column(Float)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    status_id = Column('status_id', Integer(), ForeignKey('order_statuses.id'), nullable=False)
    status = relationship("OrderStatus", back_populates="orders", lazy="selectin")
    parts = relationship("OrderParts", back_populates="order", lazy="selectin")
