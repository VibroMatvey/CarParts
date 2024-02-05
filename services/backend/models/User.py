from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from config.db import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    login = Column(String, unique=True)
    password = Column(String)
    role_id = Column('role_id', Integer(), ForeignKey('roles.id'), nullable=False)
    role = relationship("Role", back_populates="users", lazy="selectin")
