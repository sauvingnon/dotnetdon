# services/3x_ui/xui_service.py

from app.services.db.client import client
from typing import Optional

async def get_online_clients() -> Optional[dict]:
    """
    Получить клиентов онлайн.
    """
    response = await client.get(
        "/online_clients"
    )
    if response.status_code == 404:
        return None
    response.raise_for_status()
    return response.json()

async def create_client(tg_username: str) -> Optional[dict]:
    """
    Создать нового клиента.
    """
    response = await client.post(
        "/add_client",
        json={
            "tg_username": tg_username
        }
    )
    response.raise_for_status()
    return response.json()
