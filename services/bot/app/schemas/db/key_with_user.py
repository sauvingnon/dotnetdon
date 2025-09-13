from typing import Optional
from pydantic import BaseModel
from datetime import datetime
from .user import User

class KeyWithUser(BaseModel):
    id: int
    sub_url: Optional[str] = None
    client_email: Optional[str] = None
    web_id: Optional[str] = None
    active_until: datetime
    user_id: int
    user: User
    order_id: Optional[int] = None
    warned: bool
    expired_warned: bool