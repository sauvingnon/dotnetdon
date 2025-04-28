from app.services.db.client import client
from typing import Optional, List
from httpx import HTTPStatusError, ConnectTimeout, RequestError
from app.services.db.pyndantic import to_pydantic_model, to_pydantic_models
from app.models.user import User

entity_schema = "users"

async def create_user(tg_id: int, tg_username: str) -> dict:
    """
    Создать нового пользователя.
    """
    try:
        response = await client.post(
            f"{entity_schema}/create_user",
            json={"tg_id": tg_id, "tg_username": tg_username}
        )
        response.raise_for_status()
        user_data = response.json()
        return to_pydantic_model(User, user_data)
    except HTTPStatusError as e:
        if e.response.status_code == 404:
            return None
        raise  

    except (ConnectTimeout, RequestError) as e:
        print(f"Ошибка при подключении или запросе: {e}")
        return None 

    except Exception as e:
        print(f"Неизвестная ошибка: {e}")
        return None 

async def get_user_for_tg_id(tg_id: int) -> Optional[dict]:
    """
    Получить пользователя по его Telegram ID.
    """
    try:
        response = await client.get(
            f"{entity_schema}/get_user_for_tg_id",
            params={"tg_id": tg_id}
        )
        if response.status_code == 404:
            return None
        response.raise_for_status()
        user_data = response.json()
        return to_pydantic_model(User, user_data)
    except HTTPStatusError as e:
        if e.response.status_code == 404:
            return None
        raise  

    except (ConnectTimeout, RequestError) as e:
        print(f"Ошибка при подключении или запросе: {e}")
        return None 

    except Exception as e:
        print(f"Неизвестная ошибка: {e}")
        return None 

async def get_user_for_user_id(user_id: int) -> Optional[dict]:
    """
    Получить пользователя по внутреннему user_id.
    """
    try:
        response = await client.get(
            f"{entity_schema}/get_user_for_user_id",
            params={"user_id": user_id}
        )
        if response.status_code == 404:
            return None
        response.raise_for_status()
        user_data = response.json()
        return to_pydantic_model(User, user_data)
    except HTTPStatusError as e:
        if e.response.status_code == 404:
            return None
        raise  

    except (ConnectTimeout, RequestError) as e:
        print(f"Ошибка при подключении или запросе: {e}")
        return None 

    except Exception as e:
        print(f"Неизвестная ошибка: {e}")
        return None 

async def get_users() -> List[dict]:
    """
    Получить всех пользователей.
    """
    try:
        response = await client.get(f"{entity_schema}/get_users")
        response.raise_for_status()
        users_data = response.json()
        return to_pydantic_models(User, users_data)
    except HTTPStatusError as e:
        if e.response.status_code == 404:
            return None
        raise  

    except (ConnectTimeout, RequestError) as e:
        print(f"Ошибка при подключении или запросе: {e}")
        return None 

    except Exception as e:
        print(f"Неизвестная ошибка: {e}")
        return None 
