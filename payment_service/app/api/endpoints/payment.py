from fastapi import APIRouter
from app.services import payment_service
from app.api.schemas.paymentRequest import PaymentRequest

router = APIRouter(
    prefix="/payment",
    tags=["payment"],
)

@router.post("/add_payment")
async def add_payment(payment: PaymentRequest):
    return await payment_service.create_payment(
        email=payment.email,
        description=payment.description,
        return_url=payment.return_url,
        amount=payment.amount
    )

@router.get("/check_payment")
async def check_payment(payment_id):
    return await payment_service.payment_is_paid(payment_id=payment_id)