# app/api/endpoints/users.py

from fastapi import APIRouter
from app.crud import user_crud

router = APIRouter()

@router.get("/get_user_for_tg_id")
async def get_user(tg_id: int):
    return await user_crud.get_user_for_tg_id(tg_id)

@router.get("/get_users")
async def get_users():
    return await user_crud.get_users()
