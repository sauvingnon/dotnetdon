# app/api/endpoints/orders.py

from fastapi import APIRouter
from app.crud import order_crud
from app.api.schemas.order import OrderCreate, OrderUpdate

router = APIRouter()

@router.post("/create_order")
async def create_order(order: OrderCreate):
    return await order_crud.create_order(order.user_id, order.platform, order.payment_id, order.duration, order.order_price, order.is_paid)

@router.get("/get_orders")
async def get_orders(user_id: int):
    return await order_crud.get_orders(user_id)

@router.get("/get_order")
async def get_order(order_id: int):
    return await order_crud.get_order(order_id)

@router.patch("/update_order")
async def update_order(data: OrderUpdate):
    return await order_crud.update_order(data.order_id, data.payment_id, data.order_price, data.is_paid, data.platform)

@router.get("/get_order_by_payment_id")
async def get_order_by_payment_id(payment_id: str):
    return await order_crud.get_order_by_payment_id(payment_id)