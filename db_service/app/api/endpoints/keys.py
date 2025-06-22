# app/api/endpoints/keys.py

from fastapi import APIRouter
from app.crud import key_crud, order_crud, user_crud
from app.api.schemas.key import KeyCreate
from app.models.models import ResponseData

from datetime import datetime

router = APIRouter()

# Получить ключ по заказу
@router.get("/get_key_for_order_id")
async def get_key_for_order_id(order_id: int):
    return await key_crud.get_key_for_order_id(order_id)

# Получить ключ по его специальному id
@router.get("/get_key_for_special_id")
async def get_key_for_special_id(key_special_id: str):
    return await key_crud.get_key_for_special_id(key_special_id)

# Создание ключа
@router.post("/create_key")
async def create_key(key: KeyCreate):
    return await key_crud.create_key(key.key_content, key.user_id, key.order_id)

# Получение данных о подписке по специальному id ключа, так как метод один, это не тянет на выделение
# отдельного контейнера
@router.get("/get_data_for_special_id")
async def get_data_for_special_id(key_special_id: str):
    key = await key_crud.get_key_for_special_id(key_special_id)
    user = await user_crud.get_user_for_user_id(key.user_id)
    order = await order_crud.get_order(key.order_id)

    today = datetime.now().date()
    delta_days = (key.active_until - today).days

    days_str = f"{delta_days} дней" if delta_days >= 0 else "Истёк"

    response = ResponseData(
        user_name=user.tg_username,
        user_status="Активен" if delta_days >= 0 else "Неактивен",
        is_premium="Да" if user.is_premium else "Нет",
        date_for_end=key.active_until.isoformat(),
        days_for_end=days_str,
        query_date=today.isoformat(),
        key_content=key.key_content,
    )

    return response.dict()

    

