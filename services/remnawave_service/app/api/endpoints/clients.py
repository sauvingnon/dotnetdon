import datetime
from fastapi import APIRouter
from app.services import remnawave_service
from app.api.schemas.client import ClientCreate, TrialRequest, ClientUpdate

router = APIRouter(
    prefix="/remnawave",
    tags=["remnawave"],
)

@router.post("/add_client")
async def add_client(client: ClientCreate):
    return await remnawave_service.add_new_client(client.tg_username, client.duration, client.trial_duration)

# @router.patch("/update_client")
# async def update_client(client: ClientUpdate):
#     return await remnawave_service.update_client(client_email=client.client_email, new_duration=client.new_duration)

# @router.get("/online_clients")
# async def online_clients():
#     clients = await remnawave_service.get_clients_online()
#     return {"online_clients": clients}

# @router.post("/give_trial")
# async def give_trial(req: TrialRequest):
#     client = await remnawave_service.get_client_by_username(req.tg_username)
#     if not client:
#         return {"error": "Клиент не найден"}

#     success = await remnawave_service.give_trial(client.id, req.days)
#     if success:
#         return {"ok": True, "trial_until": (datetime.utcnow() + datetime.timedelta(days=req.days)).isoformat()}
#     return {"error": "Не удалось выдать триал"}