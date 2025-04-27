# app/api/endpoints/orders.py

from fastapi import APIRouter
from app.crud import order_crud
from app.api.schemas.order import OrderCreate

router = APIRouter()

@router.post("/create_order")
async def create_order(order: OrderCreate):
    return await order_crud.create_order(order.user_id, order.platform, order.order_price, order.is_paid)

@router.get("/get_orders")
async def get_orders(user_id: int):
    return await order_crud.get_orders(user_id)

@router.get("/get_order")
async def get_order(order_id: int):
    return await order_crud.get_order(order_id)

@router.get("/update_order")
async def update_order(order_id: int, order_price: int = None, is_paid: bool = None, platform: str = None):
    return await order_crud.update_order(order_id, order_price, is_paid, platform)

