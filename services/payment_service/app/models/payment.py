from pydantic import BaseModel, Field
from typing import Optional, Dict

class Amount(BaseModel):
    currency: str
    value: str

class Confirmation(BaseModel):
    type: str
    return_url: Optional[str] = Field(None, alias='confirmation_url')

class PaymentMethod(BaseModel):
    # тут опиши поля, которые реально приходят, или Optional, если не знаешь
    pass

class Recipient(BaseModel):
    account_id: str
    gateway_id: str

class YooKassaPayment(BaseModel):
    id: str
    status: str
    paid: bool
    amount: Amount
    confirmation: Confirmation
    created_at: str
    description: Optional[str]
    metadata: Dict[str, str]
    payment_method: Optional[PaymentMethod] = None  # чтобы не падало, если его нет
    recipient: Recipient
    refundable: bool
    test: bool
