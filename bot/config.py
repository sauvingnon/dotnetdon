import os
from dotenv import load_dotenv

# Загружаем переменные окружения из .env файла
load_dotenv()

# Теперь можешь обращаться к переменным окружения
BOT_TOKEN = os.getenv("BOT_TOKEN")
DB_SERVICE_URL = os.getenv("DB_SERVICE_URL")
URL_WEBSITE = os.getenv("URL_WEBSITE")
ADMIN_ID = os.getenv("ADMIN_ID")
PANEL_SERVICE_URL = os.getenv("PANEL_SERVICE_URL")