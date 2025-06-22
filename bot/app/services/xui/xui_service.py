# services/3x_ui/xui_service.py

from app.services.xui.client import client
from typing import Optional
from app.models.xui.client import Client
from app.models.pyndantic import to_pydantic_model

entity_schema = "xui"

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

async def create_client(tg_username: str) -> Optional[Client]:
    """
    Создать нового клиента.
    """
    response = await client.post(
        f"{entity_schema}/add_client",
        json={
            "tg_username": tg_username
        }
    )
    response.raise_for_status()
    client_data = response.json()
    return to_pydantic_model(Client, client_data)
