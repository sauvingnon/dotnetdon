# app/main.py

from fastapi import FastAPI
from app.api.endpoints import users, orders, keys

app = FastAPI(debug=True)

# Подключаем роутеры
app.include_router(users.router, prefix="/users", tags=["Users"])
app.include_router(orders.router, prefix="/orders", tags=["Orders"])
app.include_router(keys.router, prefix="/keys", tags=["Keys"])
