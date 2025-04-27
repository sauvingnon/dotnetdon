# app/api/endpoints/keys.py

from fastapi import APIRouter
from app.crud import key_crud
from app.api.schemas.key import KeyCreate

router = APIRouter()

@router.get("/get_key_for_order_id")
async def get_key_for_order_id(order_id: int):
    return await key_crud.get_key_for_order_id(order_id)

@router.get("/get_key_for_special_id")
async def get_key_for_special_id(key_special_id: int):
    return await key_crud.get_key_for_special_id(key_special_id)

@router.post("/create_key")
async def create_key(key: KeyCreate):
    return await key_crud.create_key(key.key_content, key.user_id, key.order_id)

