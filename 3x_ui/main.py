# main.py

from fastapi import FastAPI
from app.api.endpoints import clients

app = FastAPI(debug=True)

# Подключаем роутеры
app.include_router(clients.router)
