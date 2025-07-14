from fastapi import APIRouter
from payment_service.app.services import payment_service
from app.api.schemas.paymentRequest import PaymentRequest

router = APIRouter(
    prefix="/payment",
    tags=["payment"],
)

@router.post("/add_payment")
async def add_payment(payment: PaymentRequest):
    payment = await payment_service.create_payment(email=payment.email,
                                                  description=payment.description,
                                                   return_url=payment.return_url,
                                                    amount=payment.amount )
    if payment:
        return payment
    return {"error": "Не удалось создать заявку на оплату"}

@router.get("/check_payment")
async def check_payment(payment_id):
    is_paid = await payment_service.payment_is_paid(payment_id=payment_id)
    return {"is_paid": is_paid}