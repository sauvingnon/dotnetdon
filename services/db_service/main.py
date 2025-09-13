# app/main.py

from fastapi import FastAPI
from app.api.endpoints import users, orders, keys
import sentry_sdk
from sentry_sdk.integrations.asgi import SentryAsgiMiddleware

# Подготовка Sentry
sentry_sdk.init(
    dsn="https://51514aae0f917f7ae3c3fb747d8b5e0a@o4509921859076096.ingest.de.sentry.io/4509921886928976",
    environment="db_service",
    send_default_pii=False,  # отключаем автоматическую отправку личных данных
    enable_logs=True, # Включаем захват логов логгера.
    traces_sample_rate=1.0,  # захватывать 100% транзакций для трассировки
    before_send=lambda event, hint: sanitize_event(event, hint),
)

# Фильтрация чувствтельных данных
def sanitize_event(event, hint):
    """
    Фильтруем чувствительные данные:
    - удаляем headers
    - удаляем cookies
    - оставляем только сообщение, трейсбек и контекст
    """
    # Очистка заголовков запросов
    if "request" in event:
        request = event["request"]
        request.pop("headers", None)
        request.pop("cookies", None)
        request.pop("data", None)  # тело запроса
    return event

# Поднимаем само приложение
app = FastAPI(debug=True)
# Настраиваем перехват всех исключений выброшенных во вне
app.add_middleware(SentryAsgiMiddleware)

# Подключаем роутеры
app.include_router(users.router, prefix="/users", tags=["Users"])
app.include_router(orders.router, prefix="/orders", tags=["Orders"])
app.include_router(keys.router, prefix="/keys", tags=["Keys"])
