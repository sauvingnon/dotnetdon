from pydantic import BaseModel

class ClientCreate(BaseModel):
    tg_username: str

class TrialRequest(BaseModel):
    user_id: str
    days: int