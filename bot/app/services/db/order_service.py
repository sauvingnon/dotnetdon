from app.services.db.client import client
from typing import Optional, List
from httpx import HTTPStatusError, ConnectTimeout, RequestError
from app.models.pyndantic import to_pydantic_model, to_pydantic_models
from app.models.db.order import Order

entity_schema = "orders"

async def create_order(user_id: int, platform: str, order_price: int, is_paid: bool) -> Optional[Order]:
    """
    Создать новый заказ.
    """
    try:
        response = await client.post(
            f"{entity_schema}/create_order",
            json={
                "user_id": user_id,
                "platform": platform,
                "order_price": order_price,
                "is_paid": is_paid
            }
        )
        response.raise_for_status()
        order_data = response.json()
        return to_pydantic_model(Order, order_data)
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

async def get_orders(user_id: int) -> Optional[List[Order]]:
    """
    Получить все заказы пользователя.
    """
    try:
        response = await client.get(
            f"{entity_schema}/get_orders",
            params={"user_id": user_id}
        )
        response.raise_for_status()
        orders_data = response.json()
        return to_pydantic_models(Order, orders_data)
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

async def get_order(order_id: int) -> Optional[Order]:
    """
    Получить конкретный заказ по order_id.
    """
    try:
        response = await client.get(
            f"{entity_schema}/get_order",
            params={"order_id": order_id}
        )
        if response.status_code == 404:
            return None
        response.raise_for_status()
        order_data = response.json()
        return to_pydantic_model(Order, order_data)
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

async def update_order(
    order_id: int,
    order_price: Optional[int] = None,
    is_paid: Optional[bool] = None,
    platform: Optional[str] = None
) -> dict:
    """
    Обновить заказ (частичное обновление полей).
    """
    try:
        response = await client.get(
            f"{entity_schema}/update_order",
            params={
                "order_id": order_id,
                "order_price": order_price,
                "is_paid": is_paid,
                "platform": platform
            }
        )
        response.raise_for_status()
        order_data = response.json()
        return to_pydantic_model(Order, order_data)
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