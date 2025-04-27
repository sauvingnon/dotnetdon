from pydantic import BaseModel

class OrderCreate(BaseModel):
    user_id: int
    platform: str
    order_price: int
    is_paid: bool
