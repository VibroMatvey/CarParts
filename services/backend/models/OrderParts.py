from sqlalchemy import Column, Integer, Float, ForeignKey
from sqlalchemy.orm import relationship

from config.db import Base


class OrderParts(Base):
    __tablename__ = "order_parts"

    id = Column(Integer, primary_key=True, index=True)
    count = Column(Integer)
    total = Column(Float)
    part_id = Column('part_id', Integer(), ForeignKey('parts.id'), nullable=False)
    part = relationship("Part", back_populates="order_parts", lazy="selectin")
    order_id = Column('order_id', Integer(), ForeignKey('orders.id'), nullable=False)
    order = relationship("Order", back_populates="parts", lazy="selectin")
