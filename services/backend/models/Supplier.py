from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from config.db import Base


class Supplier(Base):
    __tablename__ = "suppliers"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    address = Column(String, nullable=True)
    email = Column(String, nullable=True)
    phone = Column(String, nullable=True)
    parts = relationship("Part", back_populates="supplier", lazy="selectin")
