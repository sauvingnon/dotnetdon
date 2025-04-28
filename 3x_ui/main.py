# main.py

from fastapi import FastAPI
from app.api.endpoints import xui

app = FastAPI(debug=True)

# Подключаем роутеры
app.include_router(xui.router)
