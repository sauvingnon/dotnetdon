# app/crud/key_crud.py

from sqlalchemy.future import select
from sqlalchemy.exc import SQLAlchemyError
from app.models.models import Key, User
from app.core.db import AsyncSessionLocal
from datetime import date
from dateutil.relativedelta import relativedelta
import uuid
from datetime import datetime, timezone
from typing import List

# Получить ключи пользователя
async def get_active_keys_for_tg_id(tg_id: int) -> List[Key]:
    async with AsyncSessionLocal() as session:
        try:
            result_user = await session.execute(select(User).filter(User.tg_id == tg_id))
            user = result_user.scalar()

            if user is None:
                return []
            
            now = datetime.now(timezone.utc)

            result_keys = await session.execute(
                select(Key).filter(
                    Key.user_id == user.id,
                    Key.active_until > now  # фильтрация по дате
                )
            )
            keys = result_keys.scalars().all()
            return keys

        except Exception as e:
            print(f"Ошибка: {e}")
            return []  # чтобы не возвращать None


# Получить ключ по заказу
async def get_key_for_order_id(order_id: int) -> Key:
    async with AsyncSessionLocal() as session:
        try:
            result = await session.execute(select(Key).filter(Key.order_id == order_id))
            key = result.scalar()
            return key
        except Exception as e:
            print(f"Ошибка: {e}")

# Получить ключ по спец ID
async def get_key_for_web_id(web_id: int) -> Key:
    async with AsyncSessionLocal() as session:
        try:
            result = await session.execute(select(Key).filter(Key.web_id == web_id))
            key = result.scalar()
            return key
        except Exception as e:
            print(f"Ошибка: {e}")

# Функция для создания ключа
async def create_key(user_id: int, sub_url: str, client_email: str, active_until: datetime, order_id: int = None) -> Key:
    async with AsyncSessionLocal() as session:
        try:            
            web_id = str(uuid.uuid4())
            new_key = Key(
                sub_url=sub_url,
                client_email=client_email,
                user_id=user_id,
                active_until=active_until,
                order_id=order_id,
                web_id=web_id
            )
            session.add(new_key)
            await session.commit()
            await session.refresh(new_key)
            print("Ключ добавлен")
            return new_key
        except SQLAlchemyError as e:
            print(f"Ошибка: {e}")
            await session.rollback()