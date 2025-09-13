#!/bin/sh
# Ждём пока БД поднимется
until pg_isready -h db -p 5432; do
  echo "Waiting for database..."
  sleep 1
done

# Запускаем alembic
alembic upgrade head
