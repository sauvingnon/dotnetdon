from datetime import datetime
from typing import Optional
from pydantic import BaseModel

class KeyCreate(BaseModel):
    user_id: int
    sub_url: str
    client_email: str
    active_until: datetime
    order_id: Optional[int] = None
    