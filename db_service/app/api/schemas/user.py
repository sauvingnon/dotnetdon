from pydantic import BaseModel

class UserCreate(BaseModel):
    tg_id: int
    tg_username: str
