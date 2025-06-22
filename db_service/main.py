# app/main.py

from fastapi import FastAPI
from app.api.endpoints import users, orders, keys
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(debug=True)

origins = [
    "http://localhost:3000",  # если фронт на 3000, например
    "http://127.0.0.1:3000",
    # можно "*", но это опасно для продакшна
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # или ["*"] для разработки
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Подключаем роутеры
app.include_router(users.router, prefix="/users", tags=["Users"])
app.include_router(orders.router, prefix="/orders", tags=["Orders"])
app.include_router(keys.router, prefix="/keys", tags=["Keys"])
