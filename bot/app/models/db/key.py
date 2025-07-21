from typing import Optional
from pydantic import BaseModel
from datetime import datetime

class Key(BaseModel):
    id: int
    sub_url: Optional[str]
    client_email: Optional[str]
    web_id: Optional[str]
    active_until: datetime
    user_id: int
    order_id: Optional[int]
