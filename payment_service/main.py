# main.py

from fastapi import FastAPI
from app.api.endpoints import payment

app = FastAPI(debug=True)

# Подключаем роутеры
app.include_router(payment.router)
