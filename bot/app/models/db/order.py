from pydantic import BaseModel
from datetime import date

class Order(BaseModel):
    id: int
    order_price: int
    create_date: date
    is_paid: bool
    platform: str
    user_id: int
    duration: int
