from sqlalchemy import Column, Integer, DateTime, Boolean, String, ForeignKey
from sqlalchemy.orm import relationship
from app.models.base import Base

class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, autoincrement=True)
    order_price = Column(Integer, nullable=False)
    duration = Column(Integer, nullable=False)
    create_date = Column(DateTime, nullable=False)
    is_paid = Column(Boolean, nullable=False)
    platform = Column(String, nullable=False)
    payment_id = Column(String, nullable=False)

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    user = relationship("User", back_populates="orders")

    key = relationship("Key", back_populates="order")
