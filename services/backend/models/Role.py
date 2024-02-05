from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from config.db import Base


class Role(Base):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    users = relationship("User", back_populates="role", lazy="selectin")
