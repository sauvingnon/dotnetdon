from fastapi import APIRouter
from app.api.services import xui_service

router = APIRouter(
    prefix="/xui",
    tags=["xui"],
)

@router.post("/add_client")
async def add_client(tg_username: str):
    subscription_url = await xui_service.add_new_client(tg_username)
    if subscription_url:
        return {"subscription_url": subscription_url}
    return {"error": "Не удалось создать клиента"}

@router.get("/online_clients")
async def online_clients():
    clients = await xui_service.get_clients_online()
    return {"online_clients": clients}
