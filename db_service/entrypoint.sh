#!/bin/sh

chmod +x entrypoint.sh

echo "Запускаем миграции..."
alembic upgrade head

echo "Запускаем приложение..."
exec uvicorn main:app --host 0.0.0.0 --port 8000