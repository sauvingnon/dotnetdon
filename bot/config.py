import os
from dotenv import load_dotenv

# Загружаем переменные окружения из .env файла
load_dotenv()

# Теперь можешь обращаться к переменным окружения
BOT_URL = os.getenv("BOT_URL")
PAYMENT_SERVICE_URL = os.getenv("PAYMENT_SERVICE_URL")
BOT_TOKEN = os.getenv("BOT_TOKEN")
BOT_TOKEN_TEST = os.getenv("BOT_TOKEN_TEST")
DB_SERVICE_URL = os.getenv("DB_SERVICE_URL")
URL_WEBSITE = os.getenv("URL_WEBSITE")
ADMIN_ID = os.getenv("ADMIN_ID")
PANEL_SERVICE_URL = os.getenv("PANEL_SERVICE_URL")
ADMIN_ID_2 = os.getenv("ADMIN_ID_2")
TRIAL_DURATION = int(os.getenv("TRIAL_DURATION"))