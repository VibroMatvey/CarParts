from sqlalchemy import Column, Integer, DateTime, Float, ForeignKey, String
from sqlalchemy.orm import relationship
import datetime

from config.db import Base


class Sales(Base):
    __tablename__ = "sales"

    id = Column(Integer, primary_key=True, index=True)
    total = Column(Float())
    name = Column(String())
    phone = Column(String())
    count = Column(Integer())
    created_at = Column(DateTime())
    updated_at = Column(DateTime())
    status_id = Column('status_id', Integer(), ForeignKey('sales_statuses.id'), nullable=False)
    status = relationship("SalesStatus", back_populates="sales", lazy="selectin")
    part_id = Column('part_id', Integer(), ForeignKey('parts.id'), nullable=False)
    part = relationship("Part", back_populates="sales_parts", lazy="selectin")
