# app/api/endpoints/users.py

from fastapi import APIRouter
from app.crud import user_crud
from app.api.schemas.user import UserCreate, UserUpdate

router = APIRouter()

@router.post("/create_user")
async def create_user(create_request: UserCreate):
    return await user_crud.create_user(create_request.tg_id, create_request.tg_username)

@router.post("/update_user")
async def update_user(update_request: UserUpdate):
    return await user_crud.update_user(update_request.user_tg_id, update_request.new_email, update_request.new_test_used, update_request.new_is_premium)

@router.get("/get_user_for_tg_id")
async def get_user_for_tg_id(tg_id: int):
    return await user_crud.get_user_for_tg_id(tg_id)

@router.get("/get_user_for_user_id")
async def get_user_for_user_id(user_id: int):
    return await user_crud.get_user_for_user_id(user_id)

@router.get("/get_users")
async def get_users():
    return await user_crud.get_users()
