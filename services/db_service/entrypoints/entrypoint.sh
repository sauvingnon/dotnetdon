#!/bin/sh
echo "Запускаем приложение..."
exec uvicorn main:app --host 0.0.0.0 --port 8000
