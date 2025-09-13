from pydantic import BaseModel

class ResponseData(BaseModel):
    user_name: str
    user_status: str
    email: str
    is_premium: str
    days_for_end: str
    date_for_end: str
    query_date: str
    key_content: str
