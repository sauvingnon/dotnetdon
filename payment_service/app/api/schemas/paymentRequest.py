from pydantic import BaseModel

class PaymentRequest(BaseModel):
    email: str
    description: str
    return_url: str
    amount: int