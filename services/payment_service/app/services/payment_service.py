import uuid
from yookassa import Configuration, Payment
from typing import Optional
from logger import logger

from config import ACCOUNT_ID, SECRET_KEY
# capture значит что сумма спишется моментально, а не будет заморожена на счету пользователя для списания в удобное время.

Configuration.configure(ACCOUNT_ID, SECRET_KEY)

# Метод для проверки статуса платежа
async def payment_is_paid(payment_id: str) -> Optional[bool]:
    try:
        payment = Payment.find_one(payment_id)
        logger.info(f"Статус платежа {payment_id} получен успешно: {payment.paid}")
        return payment.paid
    except Exception as e:
        logger.exception(f"Ошибка при получении статуса платежа {payment_id}: {e}")
        return None
      
# Метод создания платежа
async def create_payment(email: str, description: str, return_url: str, amount: int) -> Payment:
    try:
        # тут вызов без await, если API синхронный
        payment = Payment.create({
            "amount": {
                "value": f"{amount}.00",
                "currency": "RUB"
            },
            "confirmation": {
                "type": "redirect",
                "return_url": return_url
            },
            "capture": True,
            "description": description,
            "receipt": {
                "customer": {"email": email},
                "items": [{
                    "description": "Доступ к сервису dotNetDon Network",
                    "quantity": 1,
                    "amount": {"value": f"{amount}.00", "currency": "RUB"},
                    "vat_code": 1,
                }]
            }
        }, uuid.uuid4())

        logger.info(f"Заявка на оплату создана успешно. email: {email}, amount: {amount}")

        return payment
    except Exception as e:
        logger.exception(f"Ошибка создания платежа: {e}")
        return None
