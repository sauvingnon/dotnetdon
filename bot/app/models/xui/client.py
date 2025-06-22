from pydantic import BaseModel, Field
from typing import Union, Optional

class Client(BaseModel):
    email: str
    enable: bool
    id: Optional[Union[int, str]] = None
    password: str = ""
    inboundId: Optional[int] = None
    up: int = 0
    down: int = 0
    expiryTime: int = 0
    total: int = 0
    reset: Optional[int] = None
    flow: str = ""
    method: str = ""
    limitIp: int = 0
    subId: str = ""
    tgId: Optional[Union[int, str]] = ""
    totalGB: int = 0
    url_sub: Optional[str] = None
