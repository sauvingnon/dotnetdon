from fastapi import APIRouter
from app.services import xui_service
from app.api.schemas.client import ClientCreate, TrialRequest

router = APIRouter(
    prefix="/xui",
    tags=["xui"],
)

@router.post("/add_client")
async def add_client(client: ClientCreate):
    client = await xui_service.add_new_client(client.tg_username)
    if client:
        return client
    return {"error": "Не удалось создать клиента"}

@router.get("/online_clients")
async def online_clients():
    clients = await xui_service.get_clients_online()
    return {"online_clients": clients}

@router.post("/give_trial")
async def give_trial(req: TrialRequest):
    client = await xui_service.get_client_by_username(req.tg_username)
    if not client:
        return {"error": "Клиент не найден"}

    success = await xui_service.give_trial(client.id, req.days)
    if success:
        return {"ok": True, "trial_until": (datetime.utcnow() + timedelta(days=req.days)).isoformat()}
    return {"error": "Не удалось выдать триал"}