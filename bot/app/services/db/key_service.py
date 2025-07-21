# services/db/key.py

from datetime import datetime
from app.services.db.client import client
from typing import Optional
from httpx import HTTPStatusError, ConnectTimeout, RequestError
from app.models.pyndantic import to_pydantic_model, to_pydantic_models
from app.models.db.key import Key
from typing import List
import logging

logger = logging.getLogger(__name__)

entity_schema = "keys"

# Получить активные ключи пользователя
async def get_active_keys_for_tg_id(tg_id: int) -> Optional[List[Key]]:
    """
    Получить активные ключи пользователя.
    """
    try:
        response = await client.get(
            f"{entity_schema}/get_active_keys_for_tg_id",
            params={"tg_id": tg_id}
        )
        response.raise_for_status()
        key_data = response.json()
        return to_pydantic_models(Key, key_data) 
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

# Функция получения ключа по order_id с обработкой ошибок
async def get_key_for_order_id(order_id: int) -> Optional[Key]:
    """
    Получить ключ по order_id.
    """
    try:
        # Отправляем запрос
        response = await client.get(
            f"{entity_schema}/get_key_for_order_id",
            params={"order_id": order_id}
        )
        
        # Проверка на успешный статус ответа
        response.raise_for_status()
        
        # Преобразуем ответ в модель, если данные получены
        key_data = response.json()
        return to_pydantic_model(Key, key_data)  # Преобразуем словарь в модель Pydantic

    except HTTPStatusError as e:
        # Ошибка статуса HTTP (например, 404, 500)
        if e.response.status_code == 404:
            return None  # Если ключ не найден, возвращаем None
        raise  # Повторно выбрасываем исключение для других статусов ошибок

    except (ConnectTimeout, RequestError) as e:
        # Ошибки соединения или запроса
        print(f"Ошибка при подключении или запросе: {e}")
        return None  # Возвращаем None, так как не удалось выполнить запрос

    except Exception as e:
        # Обработка любых других непредвиденных ошибок
        print(f"Неизвестная ошибка: {e}")
        return None  # Возвращаем None в случае ошибки

async def get_key_for_special_id(key_special_id: int) -> Optional[Key]:
    """
    Получить ключ по специальному идентификатору.
    """
    try:
        response = await client.get(
            f"{entity_schema}/get_key_for_special_id",
            params={"key_special_id": key_special_id}
        )
        response.raise_for_status()
        key_data = response.json()
        return to_pydantic_model(Key, key_data) 
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

async def create_key(user_id: int, sub_url: str, client_email: str, active_until: datetime, order_id: int = None) -> Optional[Key]:
    try:
        response = await client.post(
            f"{entity_schema}/create_key",
            json={
                "user_id": user_id,
                "sub_url": sub_url,
                "client_email": client_email,
                "active_until": active_until.isoformat(),
                "order_id": order_id
            }
        )
        response.raise_for_status()
        key_data = response.json()
        return to_pydantic_model(Key, key_data)

    except HTTPStatusError as e:
        if e.response.status_code == 404:
            return None 
        logger.error(f"HTTP ошибка: {e}", exc_info=True)
        raise  

    except (ConnectTimeout, RequestError) as e:
        logger.error(f"Ошибка при подключении или запросе: {e}", exc_info=True)
        return None

    except Exception as e:
        logger.error(f"Неизвестная ошибка: {e}", exc_info=True)
        return None
