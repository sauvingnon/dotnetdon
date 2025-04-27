from pydantic import BaseModel

class KeyCreate(BaseModel):
    key_content: str
    user_id: int
    order_id: int
