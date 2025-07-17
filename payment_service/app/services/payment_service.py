import uuid
from yookassa import Configuration, Payment
from typing import Optional

from config import ACCOUNT_ID, SECRET_KEY
# capture значит что сумма спишется моментально, а не будет заморожена на счету пользователя для списания в удобное время.

Configuration.configure(ACCOUNT_ID, SECRET_KEY)

# Метод для проверки статуса платежа
async def payment_is_paid(payment_id: str) -> Optional[bool]:
    try:
        payment = Payment.find_one(payment_id)
        return payment.paid
    except Exception as e:
        print(f"[payment_is_paid] Ошибка при получении статуса платежа {payment_id}: {e}")
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
                    "description": "Доступ к сервису dotNetDon",
                    "quantity": 1,
                    "amount": {"value": f"{amount}.00", "currency": "RUB"},
                    "vat_code": 1,
                }]
            }
        }, uuid.uuid4())

        return payment
    except Exception as e:
        print("Ошибка создания платежа:", e)
        return None
