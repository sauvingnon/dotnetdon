from sqlalchemy import Column, Integer, Date, Boolean, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from pydantic import BaseModel

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True) 
    tg_id = Column(Integer, unique=True, nullable=False)
    test_used = Column(Boolean, default=False)
    tg_username = Column(String, nullable=False)
    is_premium = Column(Boolean, default=False)


    keys = relationship("Key", back_populates="user", cascade="all, delete-orphan")
    orders = relationship("Order", back_populates="user", cascade="all, delete-orphan")

class Key(Base):
    __tablename__ = "keys"

    id = Column(Integer, primary_key=True, autoincrement=True)
    key_content = Column(String, nullable=True)
    key_id = Column(String, nullable=True)
    active_until = Column(Date, nullable=False)

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    user = relationship("User", back_populates="keys")

    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)

    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)
    order = relationship("Order", back_populates="key")

class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, autoincrement=True)
    order_price = Column(Integer, nullable=False)
    create_date = Column(Date, nullable=False)
    is_paid = Column(Boolean, nullable=False)
    platform = Column(String, nullable=False)

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    user = relationship("User", back_populates="orders")


    key = relationship("Key", back_populates="order")

# Pydantic модель — не влияет на миграции
# Pydantic модель — не влияет на миграции
class ResponseData(BaseModel):
    user_name: str
    user_status: str
    is_premium: str
    days_for_end: str
    date_for_end: str
    query_date: str
    key_content: str

