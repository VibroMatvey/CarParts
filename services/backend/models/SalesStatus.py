from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from config.db import Base


class SalesStatus(Base):
    __tablename__ = "sales_statuses"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    sales = relationship("Sales", back_populates="status", lazy="selectin")
