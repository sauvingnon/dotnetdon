from sqlalchemy import Column, Integer, DateTime, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from app.models.base import Base

class Key(Base):
    __tablename__ = "keys"

    id = Column(Integer, primary_key=True, autoincrement=True)
    sub_url = Column(String, nullable=True)
    client_email = Column(String, nullable=True)
    web_id = Column(String, nullable=True)
    active_until = Column(DateTime(timezone=False), nullable=False)
    warned = Column(Boolean, nullable=False, default=False)
    expired_warned = Column(Boolean, nullable=False, default=False)

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    user = relationship("User", back_populates="keys")

    order_id = Column(Integer, ForeignKey("orders.id"), nullable=True)
    order = relationship("Order", back_populates="key")
