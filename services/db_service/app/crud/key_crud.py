# app/crud/key_crud.py

from sqlalchemy.future import select
from sqlalchemy.exc import SQLAlchemyError
from app.models import Key, User
from app.core.db import AsyncSessionLocal
import uuid
from datetime import datetime, timezone, timedelta
from typing import List
from sqlalchemy.orm import selectinload
from app.api.schemas.key import KeyUpdate
from logger import logger
from sqlalchemy.sql import func

# Функция для изменения ключа
async def update_key(new_key: KeyUpdate) -> Key:
    async with AsyncSessionLocal() as session:
        try:            
            result = await session.execute(select(Key).where(Key.id == new_key.id))
            key = result.scalars().first()
            
            if not key:
                return None

            for field, value in new_key.model_dump(exclude_unset=True).items():
                if field == "id":
                    continue
                setattr(key, field, value)

            await session.commit()
            await session.refresh(key)
            logger.info(f"Ключ обновлен успешно - {key.id}")
            return key
        except SQLAlchemyError as e:
            await session.rollback()
            logger.exception(f"Ошибка при обновлении ключа {key.id}")
            return None

# Получить все ключи для уведомления
async def get_keys_for_notifications() -> List[Key]:
    async with AsyncSessionLocal() as session:
        try:
            today = datetime.utcnow().date()

            result = await session.execute(
                select(Key)
                .options(selectinload(Key.user))
                .filter(
                    (
                        (func.date(Key.active_until) == today + timedelta(days=3)) &
                        (Key.warned.is_(False))
                    )
                    |
                    (
                        (Key.active_until <= datetime.utcnow()) &
                        (Key.expired_warned.is_(False))
                    )
                )
            )
            keys = result.scalars().all()
            logger.info(f"Ключи для уведомления получены успешно ({len(keys)})")
            return keys
        except SQLAlchemyError as e:
            logger.exception("Ошибка при получении ключей для уведомления")
            raise

# Получить активные ключи пользователя
async def get_active_keys_for_tg_id(tg_id: int) -> List[Key]:
    async with AsyncSessionLocal() as session:
        try:
            result_user = await session.execute(select(User).filter(User.tg_id == tg_id))
            user = result_user.scalar_one_or_none()

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

            logger.info(f"Активные ключи пользователя получены успешно {tg_id}")

            return keys

        except Exception as e:
            logger.exception(f"Ошибка при получении активных ключей пользователя: {e}")
            return []  # чтобы не возвращать None


# Получить ключ по заказу
async def get_key_for_order_id(order_id: int) -> Key:
    async with AsyncSessionLocal() as session:
        try:
            result = await session.execute(select(Key).filter(Key.order_id == order_id))
            key = result.scalar_one_or_none()

            logger.info(f"Ключ по заказу получен успешно - {order_id}")

            return key
        except Exception as e:
            logger.exception(f"Ошибка: {e}")

# Получить ключ по спец ID
async def get_key_for_web_id(web_id: str) -> Key:
    async with AsyncSessionLocal() as session:
        try:
            result = await session.execute(select(Key).filter(Key.web_id == web_id))
            key = result.scalar_one_or_none()
            logger.info(f"Ключ по спец идентификатору получен успешно - {web_id}")
            return key
        except Exception as e:
            logger.exception(f"Ошибка при получении ключа по спец идентификатору: {e}")
            return None

# Функция для создания ключа
async def create_key(user_id: int, sub_url: str, client_email: str, active_until: datetime, order_id: int = None) -> Key:
    async with AsyncSessionLocal() as session:
        try:            
            active_until = active_until.astimezone(timezone.utc).replace(tzinfo=None)
            web_id = str(uuid.uuid4())
            new_key = Key(
                sub_url=sub_url,
                client_email=client_email,
                user_id=user_id,
                active_until=active_until,
                order_id=order_id,
                web_id=web_id,
                warned=False,
                expired_warned=False
            )
            session.add(new_key)
            await session.commit()
            await session.refresh(new_key)
            logger.info(f"Ключ добавлен успешно.")
            return new_key
        except SQLAlchemyError as e:
            logger.exception(f"Ошибка при создании ключа: {e}")
            await session.rollback()
            return None