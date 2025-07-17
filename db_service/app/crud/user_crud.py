# app/crud/user_crud.py

from sqlalchemy.future import select
from sqlalchemy.exc import SQLAlchemyError
from app.models.models import User
from app.core.db import AsyncSessionLocal

# Создание пользователя
async def create_user(tg_id, tg_username) -> User:
    async with AsyncSessionLocal() as session:
        user = await get_user_for_tg_id(tg_id)
        if user:
            return user

        try:
            new_user = User(tg_id=tg_id, test_used=False, tg_username=tg_username)
            session.add(new_user)
            await session.commit()
            print("Пользователь добавлен")
            return new_user
        except SQLAlchemyError as e:
            print(f"Ошибка: {e}")
            await session.rollback()

# Редактирование пользователя
async def update_user(user_tg_id: int, new_email: str = None, new_test_used: bool = None, new_is_premium: bool = None) -> bool:
    async with AsyncSessionLocal() as session:

        user = await get_user_for_tg_id(user_tg_id)

        if not user:
            return False

        try:
            if new_email != None:
                user.email = new_email

            if new_test_used != None:
                user.test_used = new_test_used

            if new_is_premium != None:
                user.is_premium = new_is_premium

            session.add(user)
            await session.commit()
            print("Пользователь обновлен успешно")
            return True
        except SQLAlchemyError as e:
            print(f"Ошибка: {e}")
            await session.rollback()
            return False

# Функция для получения пользователя по ID в телеграме
async def get_user_for_tg_id(user_tg_id: int) -> User:
    async with AsyncSessionLocal() as session:
        try:
            result = await session.execute(select(User).filter(User.tg_id == user_tg_id))
            user = result.scalar()
            return user
        except SQLAlchemyError as e:
            print(f"Ошибка: {e}")

# Функция для получения пользователя по ID
async def get_user_for_user_id(user_id: int) -> User:
    async with AsyncSessionLocal() as session:
        try:
            result = await session.execute(select(User).filter(User.id == user_id))
            user = result.scalar()
            return user
        except SQLAlchemyError as e:
            print(f"Ошибка: {e}")

# Функция для получения всех пользователей
async def get_users():
    async with AsyncSessionLocal() as session:
        try:
            result = await session.execute(select(User))
            users = result.scalars().all()
            return users
        except SQLAlchemyError as e:
            print(f"Ошибка: {e}")