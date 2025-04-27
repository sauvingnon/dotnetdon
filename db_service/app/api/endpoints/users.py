# app/api/endpoints/users.py

from fastapi import APIRouter
from app.crud import user_crud
from app.api.schemas.user import UserCreate

router = APIRouter()

@router.post("/create_user")
async def create_user(user: UserCreate):
    return await user_crud.create_user(user.tg_id, user.tg_username)

@router.get("/get_user_for_tg_id")
async def get_user_for_tg_id(tg_id: int):
    return await user_crud.get_user_for_tg_id(tg_id)

@router.get("/get_user_for_user_id")
async def get_user_for_user_id(user_id: int):
    return await user_crud.get_user_for_user_id(user_id)

@router.get("/get_users")
async def get_users():
    return await user_crud.get_users()
