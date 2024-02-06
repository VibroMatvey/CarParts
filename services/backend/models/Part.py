from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship

from config.db import Base


class Part(Base):
    __tablename__ = "parts"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    price = Column(Float)
    code = Column(String)
    supplier_id = Column('supplier_id', Integer(), ForeignKey('suppliers.id', ondelete='SET NULL'), nullable=True)
    supplier = relationship("Supplier", back_populates="parts", lazy="selectin")
    order_parts = relationship("OrderParts", back_populates="part", lazy="selectin")
