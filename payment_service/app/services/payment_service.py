import uuid
from yookassa import Configuration, Payment
from config import ACCOUNT_ID, SECRET_KEY
# capture значит что сумма спишется моментально, а не будет заморожена на счету пользователя для списания в удобное время.

Configuration.configure(ACCOUNT_ID, SECRET_KEY)

# Метод для проверки статуса платежа
def payment_is_paid(payment_id):
  try:
    payment = Payment.find_one(payment_id)
    return payment.paid
  except:
    print("Не удалось получить статус платежа.")
    return None
      
# Метод для создания платежа
def create_payment(email: str, description: str, return_url: str, amount: int) -> Payment:
  
  try:
    payment = Payment.create({
        "amount": {
            "value": f"{amount}.00",
            "currency": "RUB"
        },
        "confirmation": {
            "type": "redirect",
            "return_url": f"{return_url}"
        },
        "capture": True,
        "description": f"{description}",
        "receipt": {
                "customer": {
                        "email": f"{email}"
                    },
                "items": [
                  {
                    "description": "Доступ к сервису dotNetDon",
                    "quantity": 1,
                    "amount": {
                      "value": f"{amount}.00",
                      "currency": "RUB"
                    },
                    "vat_code": 1
                  }
                ]
              }
    }, uuid.uuid4())


    return payment
  
  except:
    print("Ошибка создания платежа")
    return None

