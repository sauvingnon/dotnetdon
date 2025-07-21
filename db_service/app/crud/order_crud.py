# app/crud/order_crud.py

from sqlalchemy.future import select
from sqlalchemy.exc import SQLAlchemyError
from app.models.models import Order
from app.core.db import AsyncSessionLocal
from datetime import datetime

# Создание заказа
async def create_order(user_id, platform: str, payment_id: str, duration: int, order_price=None, is_paid=None) -> Order:
    async with AsyncSessionLocal() as session:
        if not order_price:
            order_price = 0

        if not is_paid:
            is_paid = False

        create_date = datetime.now()

        try:
            new_order = Order(
                order_price=order_price,
                create_date=create_date,
                is_paid=is_paid,
                user_id=user_id,
                platform=platform,
                payment_id=payment_id,
                duration=duration
            )
            session.add(new_order)
            await session.commit()
            print("Заказ добавлен")
            return new_order
        except SQLAlchemyError as e:
            print(f"Ошибка: {e}")
            await session.rollback()

# Получение заказов пользователя
async def get_orders(user_id):
    async with AsyncSessionLocal() as session:
        try:
            result = await session.execute(select(Order).filter(Order.user_id == user_id))
            orders = result.scalars().all()
            return orders
        except SQLAlchemyError as e:
            print(f"Ошибка: {e}")

# Получение заказа 
async def get_order(order_id) -> Order:
    async with AsyncSessionLocal() as session:
        try:
            result = await session.execute(select(Order).filter(Order.id == order_id))
            order = result.scalar()
            return order
        except SQLAlchemyError as e:
            print(f"Ошибка: {e}")

# Обновление заказа
async def update_order(order_id: int = None, payment_id: str = None, order_price: int = None, is_paid: bool = None, platform: str = None) -> Order:
    async with AsyncSessionLocal() as session: 
        try:
            if order_id:
                result = await session.execute(select(Order).filter(Order.id == order_id))
            elif payment_id:
                result = await session.execute(select(Order).filter(Order.payment_id == payment_id))
            else:
                print(f"Ошибка: Не переданы аргументы для поиска заказа в базе данных.")
                return
            
            order = result.scalar()
            if order_price:
                order.order_price = order_price
            if is_paid:
                order.is_paid = is_paid
            if platform:
                order.platform = platform
            await session.commit()
            await session.refresh(order)
            return order
        except SQLAlchemyError as e:
            print(f"Ошибка: {e}")
            await session.rollback()

# Получение заказа по заявке на оплату
async def get_order_by_payment_id(payment_id: str) -> Order:
    async with AsyncSessionLocal() as session:
        try:
            result = await session.execute(select(Order).filter(Order.payment_id == payment_id))
            order = result.scalar()
            return order
        except SQLAlchemyError as e:
            print(f"Ошибка: {e}")