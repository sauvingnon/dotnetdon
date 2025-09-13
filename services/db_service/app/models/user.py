from sqlalchemy import Column, Integer, Boolean, String
from sqlalchemy.orm import relationship
from app.models.base import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True) 
    tg_id = Column(Integer, unique=True, nullable=False)
    test_used = Column(Boolean, default=False)
    tg_username = Column(String, nullable=False)
    email = Column(String, nullable=True)
    is_premium = Column(Boolean, default=False)

    keys = relationship("Key", back_populates="user", cascade="all, delete-orphan")
    orders = relationship("Order", back_populates="user", cascade="all, delete-orphan")
