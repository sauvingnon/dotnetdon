# app/crud/key_crud.py

from sqlalchemy.future import select
from sqlalchemy.exc import SQLAlchemyError
from app.models.models import Key
from app.core.db import AsyncSessionLocal
from datetime import date
from dateutil.relativedelta import relativedelta
import uuid

# Получить ключ по заказу
async def get_key_for_order_id(order_id: int):
    async with AsyncSessionLocal() as session:
        try:
            result = await session.execute(select(Key).filter(Key.order_id == order_id))
            key = result.scalar()
            return key
        except Exception as e:
            print(f"Ошибка: {e}")

# Получить ключ по спец ID
async def get_key_for_special_id(key_special_id: int):
    async with AsyncSessionLocal() as session:
        try:
            result = await session.execute(select(Key).filter(Key.key_id == key_special_id))
            key = result.scalar()
            return key
        except Exception as e:
            print(f"Ошибка: {e}")

# Функция для создания ключа
async def create_key(key_content: str, user_id: int, order_id: int):
    async with AsyncSessionLocal() as session:
        try:
            date_add_month = date.today() + relativedelta(months=1)
            key_id = str(uuid.uuid4())
            new_key = Key(
                key_content=key_content,
                key_id=key_id,
                user_id=user_id,
                active_until=date_add_month,
                order_id=order_id
            )
            session.add(new_key)
            await session.commit()
            await session.refresh(new_key)
            print("Ключ добавлен")
            return new_key.id
        except SQLAlchemyError as e:
            print(f"Ошибка: {e}")
            await session.rollback()