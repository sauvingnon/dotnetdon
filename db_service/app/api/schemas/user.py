from pydantic import BaseModel
from typing import Optional

class UserCreate(BaseModel):
    tg_id: int
    tg_username: str
    
class UserUpdate(BaseModel):
    user_tg_id: int
    new_email: Optional[str] = None
    new_test_used: Optional[bool] = None
    new_is_premium: Optional[bool] = None
