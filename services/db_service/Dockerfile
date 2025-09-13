FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt . 
RUN pip install -r requirements.txt

COPY . .

# скрипты остаются для ручного запуска, но ENTRYPOINT не нужен
RUN chmod +x /app/entrypoints/entrypoint.sh /app/entrypoints/migrate.sh
RUN apt-get update && apt-get install -y postgresql-client

# убираем ENTRYPOINT
# ENTRYPOINT ["sh", "-c"]
# CMD тоже убираем, будем указывать command в docker-compose
