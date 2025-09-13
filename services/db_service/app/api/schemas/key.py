from datetime import datetime
from typing import Optional
from pydantic import BaseModel

class KeyCreate(BaseModel):
    user_id: int
    sub_url: str
    client_email: str
    active_until: datetime
    order_id: Optional[int] = None
    
class KeyUpdate(BaseModel):
    id: int
    sub_url: Optional[str] = None
    client_email: Optional[str] = None
    web_id: Optional[str] = None
    active_until: Optional[datetime] = None
    warned: Optional[bool] = None
    expired_warned: Optional[bool] = None
    order_id: Optional[int] = None

    