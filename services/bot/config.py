import os
from dotenv import load_dotenv

# Загружаем переменные окружения из .env файла
load_dotenv()

# Теперь можешь обращаться к переменным окружения
BOT_URL = os.getenv("BOT_URL")
BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = os.getenv("ADMIN_ID")
REMNAWAVE_PANEL_SERVICE_URL = os.getenv("REMNAWAVE_PANEL_SERVICE_URL")
ADMIN_ID_2 = os.getenv("ADMIN_ID_2")
TRIAL_DURATION_MONTHS = int(os.getenv("TRIAL_DURATION_MONTHS"))