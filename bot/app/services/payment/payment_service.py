# services/payment/payment_service.py

from typing import Optional

import httpx
from app.services.payment.client import client
from httpx import AsyncClient, HTTPStatusError
from app.models.payment.payment_request import AddPaymentRequest
from app.models.payment.payment_response import YooKassaPayment
from app.models.pyndantic import to_pydantic_model

entity_schema = "payment"

async def add_payment(request: AddPaymentRequest) -> Optional[YooKassaPayment]:
    """
    Отправить запрос на создание оплаты в payment-сервис.
    """
    try:
        response = await client.post(
            f"{entity_schema}/add_payment",
            json={
                "email": request.email,
                "description": request.description,
                "return_url": request.return_url,
                "amount": request.amount,
            }
        )
        response.raise_for_status()

        # ВАЖНО: .json() — синхронный метод
        data = response.json()
        return to_pydantic_model(YooKassaPayment, data)

    except httpx.HTTPStatusError as e:
        print(f"HTTP ошибка: {e.response.status_code} — {e.response.text}")
        return None

    except httpx.RequestError as e:
        print(f"Ошибка при соединении с payment-сервисом: {str(e)}")
        return None

    except Exception as e:
        print(f"Неожиданная ошибка при создании оплаты: {str(e)}")
        return None

    
async def check_payment(payment_id: str):
    """
    Проверить статус заявки на оплату.
    """
    try:
        response = await client.get(
            f"{entity_schema}/check_payment",
            params={"payment_id": payment_id}  # 👈 вот так передаём данные
        )

        response.raise_for_status()

        data = response.json()
        return data

    except HTTPStatusError as e:
        print(f"Ошибка от сервиса: {e.response.status_code} — {e.response.text}")
        return None

    except Exception as e:
        print(f"Неожиданная ошибка: {e}")
        return None