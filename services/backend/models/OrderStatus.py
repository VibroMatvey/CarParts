from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from config.db import Base


class OrderStatus(Base):
    __tablename__ = "order_statuses"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    orders = relationship("Order", back_populates="status", lazy="selectin")
