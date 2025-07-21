from pydantic import BaseModel
from typing import Optional

class ClientCreate(BaseModel):
    tg_username: str
    duration: Optional[int] = None
    trial_duration: Optional[int] = None

class ClientUpdate(BaseModel):
    client_email: str
    new_duration: Optional[int] = None

class TrialRequest(BaseModel):
    user_id: str
    days: int