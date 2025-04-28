from typing import Optional
from pydantic import BaseModel
from datetime import date

class Key(BaseModel):
    id: int
    key_content: Optional[str]
    key_id: Optional[str]
    active_until: date
    user_id: int
    order_id: Optional[int]
