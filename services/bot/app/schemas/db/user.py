from typing import Optional, List
from pydantic import BaseModel
from .key import Key
from .order import Order

class User(BaseModel):
    id: int
    tg_id: int
    tg_username: str
    email: Optional[str] = None
    test_used: bool
    is_premium: bool
    keys: Optional[List[Key]] = None
    orders: Optional[List[Order]] = None

