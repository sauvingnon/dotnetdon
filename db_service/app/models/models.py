from sqlalchemy import Column, Integer, DateTime, Boolean, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from pydantic import BaseModel

Base = declarative_base()

# Пользователь сервиса
class User(Base):
    __tablename__ = "users"

    # Внутренний идентификатор
    id = Column(Integer, primary_key=True, autoincrement=True) 
    # Идентификатор в телеграмм
    tg_id = Column(Integer, unique=True, nullable=False)
    # Использован тестовый доступ
    test_used = Column(Boolean, default=False)
    # Имя пользователя в телеграмм
    tg_username = Column(String, nullable=False)
    # email для оплаты
    email = Column(String, nullable=True)
    # Это премиум пользователь
    is_premium = Column(Boolean, default=False)

    keys = relationship("Key", back_populates="user", cascade="all, delete-orphan")
    orders = relationship("Order", back_populates="user", cascade="all, delete-orphan")

# Подписка
class Key(Base):
    __tablename__ = "keys"

    # Идентификатор подписки
    id = Column(Integer, primary_key=True, autoincrement=True)
    # Подписочная ссылка пользователя
    sub_url = Column(String, nullable=True)
    # Идентификатор в панели 3x-ui
    client_email = Column(String, nullable=True)
    # Идентификатор для web
    web_id = Column(String, nullable=True)
    # Активен до
    active_until = Column(DateTime(timezone=True), nullable=False)

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    user = relationship("User", back_populates="keys")

    order_id = Column(Integer, ForeignKey("orders.id"), nullable=True)
    order = relationship("Order", back_populates="key")

# Заказ
class Order(Base):
    __tablename__ = "orders"

    # Идентификатор заказа
    id = Column(Integer, primary_key=True, autoincrement=True)
    # Стоимость заказа
    order_price = Column(Integer, nullable=False)
    # Срок действия подписки
    duration = Column(Integer, nullable=False)
    # Дата создания заказа
    create_date = Column(DateTime, nullable=False)
    # Заказ оплачен
    is_paid = Column(Boolean, nullable=False)
    # Платформа заказа
    platform = Column(String, nullable=False)
    # Идентификатор заявки на оплату
    payment_id = Column(String, nullable=False)

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    user = relationship("User", back_populates="orders")


    key = relationship("Key", back_populates="order")

# Pydantic модель — не влияет на миграции
class ResponseData(BaseModel):
    user_name: str
    user_status: str
    email: str
    is_premium: str
    days_for_end: str
    date_for_end: str
    query_date: str
    key_content: str

