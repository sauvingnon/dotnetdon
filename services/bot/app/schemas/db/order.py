from pydantic import BaseModel
from datetime import datetime

class Order(BaseModel):
    id: int
    order_price: int
    duration: int
    create_date: datetime
    is_paid: bool
    platform: str
    user_id: int
    
