# services/remnawave/remnawave_service.py

from app.services.remnawave.client import client
from typing import Optional
from app.schemas.pyndantic import to_pydantic_model
from app.schemas.remnawave.user import UserResponseDto
from app.schemas.remnawave.addreq import ClientCreate

entity_schema = "remnawave"

async def get_online_clients() -> Optional[dict]:
    """
    Получить клиентов онлайн.
    """
    response = await client.get(
        f"{entity_schema}/online_clients"
    )
    if response.status_code == 404:
        return None
    response.raise_for_status()
    return response.json()

async def create_client(req: ClientCreate) -> Optional[UserResponseDto]:
    """
    Создать нового клиента.
    """
    response = await client.post(
        f"{entity_schema}/add_client",
        json=req.dict()
    )
    response.raise_for_status()
    client_data = response.json()
    return to_pydantic_model(UserResponseDto, client_data)