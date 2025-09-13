from pydantic import BaseModel

class AddPaymentRequest(BaseModel):
    email: str
    description: str
    return_url: str
    amount: int
