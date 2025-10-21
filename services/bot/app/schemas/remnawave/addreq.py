from pydantic import BaseModel

class ClientCreate(BaseModel):
    tg_id: int | None
    tg_username: str
    duration: int
    description: str | None