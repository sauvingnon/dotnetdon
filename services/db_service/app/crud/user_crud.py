# app/crud/user_crud.py

from sqlalchemy.future import select
from sqlalchemy.exc import SQLAlchemyError
from app.models.user import User
from app.core.db import AsyncSessionLocal
from logger import logger

# Создание пользователя
async def create_user(tg_id, tg_username) -> User:
    async with AsyncSessionLocal() as session:
        try:
            user = await get_user_for_tg_id(tg_id)
            if user:
                return user
            
            new_user = User(tg_id=tg_id, test_used=False, tg_username=tg_username)
            session.add(new_user)
            await session.commit()
            logger.info(f"Пользователь добавлен успешно - {tg_id}:{tg_username}")
            return new_user
        except SQLAlchemyError as e:
            logger.exception(f"Ошибка при добавлении пользователя - {tg_id}:{tg_username}: {e}")
            await session.rollback()
            return None

# Редактирование пользователя
async def update_user(user_tg_id: int, new_email: str = None, new_test_used: bool = None, new_is_premium: bool = None) -> bool:
    async with AsyncSessionLocal() as session:
        try:

            user = await get_user_for_tg_id(user_tg_id)

            if not user:
                return False

            if new_email != None:
                user.email = new_email

            if new_test_used != None:
                user.test_used = new_test_used

            if new_is_premium != None:
                user.is_premium = new_is_premium

            session.add(user)
            await session.commit()
            logger.info(f"Пользователь обновлен успешно {user_tg_id}")
            return True
        except SQLAlchemyError as e:
            logger.exception(f"Ошибка при обновлении пользователя: {e}")
            await session.rollback()
            return False

# Функция для получения пользователя по ID в телеграме
async def get_user_for_tg_id(user_tg_id: int) -> User:
    async with AsyncSessionLocal() as session:
        try:
            result = await session.execute(select(User).filter(User.tg_id == user_tg_id))
            user = result.scalar()
            logger.info(f"Пользователь получен успешно. {user_tg_id}")
            return user
        except SQLAlchemyError as e:
            logger.exception(f"Ошибка при получении пользователя: {e}")
            return None

# Функция для получения пользователя по ID
async def get_user_for_user_id(user_id: int) -> User:
    async with AsyncSessionLocal() as session:
        try:
            result = await session.execute(select(User).filter(User.id == user_id))
            user = result.scalar()
            logger.info(f"Пользователь получен успешно. {user_id}")
            return user
        except SQLAlchemyError as e:
            logger.exception(f"Ошибка при получении пользователя: {e}")
            return None

# Функция для получения всех пользователей
async def get_users():
    async with AsyncSessionLocal() as session:
        try:
            result = await session.execute(select(User))
            users = result.scalars().all()
            logger.info(f"Пользователи получен успешно.")
            return users
        except SQLAlchemyError as e:
            logger.exception(f"Ошибка при получении пользователей: {e}")
            return None