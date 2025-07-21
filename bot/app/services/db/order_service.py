from app.services.db.client import client
from typing import Optional, List
from httpx import HTTPStatusError, ConnectTimeout, RequestError
from app.models.pyndantic import to_pydantic_model, to_pydantic_models
from app.models.db.order import Order

entity_schema = "orders"

async def create_order(user_id: int, platform: str, order_price: int, is_paid: bool, payment_id: str, duration: int) -> Optional[Order]:
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
                "duration": duration,
                "is_paid": is_paid,
                "payment_id": payment_id
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

async def get_order_by_payment_id(payment_id: str) -> Optional[Order]:
    """
    Получить конкретный заказ по payment_id.
    """
    try:
        response = await client.get(
            f"{entity_schema}/get_order_by_payment_id",
            params={"payment_id": payment_id}
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
    order_id: Optional[int] = None,
    payment_id: Optional[str] = None,
    order_price: Optional[int] = None,
    is_paid: Optional[bool] = None,
    platform: Optional[str] = None
) -> dict:
    try:
        payload = {
            "order_id": order_id,
            "payment_id": payment_id,
            "order_price": order_price,
            "is_paid": is_paid,
            "platform": platform
        }

        # Убираем поля с None (частичное обновление)
        clean_payload = {k: v for k, v in payload.items() if v is not None}

        response = await client.patch(
            f"{entity_schema}/update_order",
            json=clean_payload
        )
        response.raise_for_status()
        data = response.json()
        return to_pydantic_model(Order, data)
    except HTTPStatusError as e:
        if e.response.status_code == 404:
            return None
        raise
    except Exception as e:
        print(f"Ошибка при обновлении заказа: {e}")
        return None
