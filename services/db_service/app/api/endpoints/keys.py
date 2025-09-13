# app/api/endpoints/keys.py

from fastapi import APIRouter
from app.crud import key_crud
from app.api.schemas.key import KeyCreate, KeyUpdate

router = APIRouter()

# Создание ключа
@router.patch("/update_key")
async def update_key(key: KeyUpdate):
    return await key_crud.update_key(key)

# Получить активные ключи пользователя
@router.get("/get_active_keys_for_tg_id")
async def get_active_keys_for_tg_id(tg_id: int):
    return await key_crud.get_active_keys_for_tg_id(tg_id)

# Получить ключи для уведомления
@router.get("/get_keys_for_notifications")
async def get_keys_for_notifications():
    return await key_crud.get_keys_for_notifications()

# Получить ключ по заказу
@router.get("/get_key_for_order_id")
async def get_key_for_order_id(order_id: int):
    return await key_crud.get_key_for_order_id(order_id)

# Получить ключ по его специальному id
@router.get("/get_key_for_web_id")
async def get_key_for_web_id(web_id: str):
    return await key_crud.get_key_for_web_id(web_id)

# Создание ключа
@router.post("/create_key")
async def create_key(key: KeyCreate):
    return await key_crud.create_key(key.user_id, key.sub_url, key.client_email, key.active_until, key.order_id)

