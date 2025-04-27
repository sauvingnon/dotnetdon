from sqlalchemy import Column, Integer, Date, Boolean, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

# Класс для хранения пользователей. Уникальность поддерживается через tg_id
class User(Base):
    __tablename__ = "User"
    # Уникальный идентификатор
    id = Column(Integer, primary_key=True, autoincrement=True) 
    # Идентификатор в Телеграм
    tg_id = Column(Integer, unique=True, nullable=False)
    # Тестовый период был использован пользователем
    test_used = Column(Boolean, default=False)
    # Имя пользователя в телеграм.
    tg_username = Column(String, nullable=False)
    # Метка премиум пользователя
    is_premium = Column(Boolean, default=False)
    # Путь до ключа, закрепленного за пользователем
    keys = relationship("Key", back_populates="user", cascade="all, delete-orphan")
     # Путь до заказа, закрепленного за пользователем
    orders = relationship("Order", back_populates="user", cascade="all, delete-orphan")

# Класс ключей, у пользователя может быть несколько ключей
class Key(Base):
    __tablename__ = "Key"
    # Уникальный идентификатор
    id = Column(Integer, primary_key=True, autoincrement=True)
    # Ключ пользователя
    key_content = Column(String, nullable=True)
    # Идентификатор ключа для запроса его с фронта
    key_id = Column(String, nullable=True)
    # Дата, до которой активна подписка
    active_until = Column(Date, nullable=False)
    # Ссылка на пользователя
    user_id = Column(Integer, ForeignKey("User.id"))
    user = relationship("User", back_populates="keys")
    # Ссылка на заказ
    order_id = Column(Integer, ForeignKey("Order.id"))
    order = relationship("Order", back_populates="key")

# Класс для процесса оформления заказа на ключ, если в течении суток не оплачено - можно удалить.
class Order(Base):
    __tablename__ = "Order"
    # Уникальный идентификатор
    id = Column(Integer, primary_key=True, autoincrement=True)
    # Сумма заказа
    order_price = Column(Integer, nullable=False)
    # Дата создания заказа
    create_date = Column(Date, nullable=False)
    # Статус заказа
    is_paid = Column(Boolean, nullable=False)
    # Целевая платформа заказа
    platform = Column(String, nullable=False)
    # Ссылка на пользователя
    user_id = Column(Integer, ForeignKey("User.id"))
    user = relationship("User", back_populates="orders")
    
    key = relationship("Key", back_populates="order")