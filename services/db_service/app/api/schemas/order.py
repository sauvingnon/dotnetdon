from pydantic import BaseModel
from typing import Optional

class OrderCreate(BaseModel):
    user_id: int
    platform: str
    order_price: int
    is_paid: bool
    payment_id: str
    duration: int

class OrderUpdate(BaseModel):
    order_id: Optional[int] = None
    payment_id: Optional[str] = None
    order_price: Optional[int] = None
    is_paid: Optional[bool] = None
    platform: Optional[str] = None