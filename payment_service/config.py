import os
from dotenv import load_dotenv

# Загружаем переменные окружения из .env файла
load_dotenv()

# Платежный токен
PROVIDER_TOKEN = os.getenv("PROVIDER_TOKEN")
# ID магазина в ЮКасса
ACCOUNT_ID = os.getenv("ACCOUNT_ID")
# Секретный ключ в ЮКасса
SECRET_KEY = os.getenv("SECRET_KEY")