# app/crud/order_crud.py

from typing import List
from sqlalchemy.future import select
from sqlalchemy.exc import SQLAlchemyError
from app.models.order import Order
from app.core.db import AsyncSessionLocal
from datetime import datetime
from logger import logger

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
            logger.info(f"Заказ добавлен успешно - {new_order.id}")
            return new_order
        except SQLAlchemyError as e:
            logger.exception(f"Ошибка при создании заказа: {e}")
            await session.rollback()
            return None

# Получение заказов пользователя
async def get_orders(user_id) -> List[Order]:
    async with AsyncSessionLocal() as session:
        try:
            result = await session.execute(select(Order).filter(Order.user_id == user_id))
            orders = result.scalars().all()
            logger.info(f"Заказы пользователя получены {user_id}")
            return orders
        except SQLAlchemyError as e:
            logger.exception(f"Ошибка при получении заказов пользователя: {e}")
            return None

# Получение заказа 
async def get_order(order_id) -> Order:
    async with AsyncSessionLocal() as session:
        try:
            result = await session.execute(select(Order).filter(Order.id == order_id))
            order = result.scalar()
            logger.info(f"Заказ получен успешно {order_id}")
            return order
        except SQLAlchemyError as e:
            logger.exception(f"Ошибка получении заказа: {e}")
            return None

# Обновление заказа
async def update_order(order_id: int = None, payment_id: str = None, order_price: int = None, is_paid: bool = None, platform: str = None) -> Order:
    async with AsyncSessionLocal() as session: 
        try:
            if order_id:
                result = await session.execute(select(Order).filter(Order.id == order_id))
            elif payment_id:
                result = await session.execute(select(Order).filter(Order.payment_id == payment_id))
            else:
                logger.error("Ошибка: Не переданы аргументы для поиска заказа в базе данных.")
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
            logger.info(f"Заказ обновлен успешно.")
            return order
        except SQLAlchemyError as e:
            logger.exception(f"Ошибка при обновлении заказа: {e}")
            await session.rollback()
            return None

# Получение заказа по заявке на оплату
async def get_order_by_payment_id(payment_id: str) -> Order:
    async with AsyncSessionLocal() as session:
        try:
            result = await session.execute(select(Order).filter(Order.payment_id == payment_id))
            order = result.scalar()
            logger.info(f"Заказ {order.id} был успешно получен по заявке на оплату {payment_id}")
            return order
        except SQLAlchemyError as e:
            logger.exception(f"Ошибка при получении заказа по заявке на оплату: {e}")
            return None