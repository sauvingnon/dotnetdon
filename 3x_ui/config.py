import os
from dotenv import load_dotenv

# Загружаем переменные окружения из .env файла
load_dotenv()

# Теперь можешь обращаться к переменным окружения
# URL_FOR_PANEL = os.getenv("URL_FOR_LOCAL")
# URL_FOR_PANEL = os.getenv("URL_FOR_SERVER")
URL_FOR_PANEL = os.getenv("URL_FOR_CONTAINER")
URL_SUBSCRIPTION = os.getenv("URL_SUBSCRIPTION")
PANEL_LOGIN = os.getenv("PANEL_LOGIN")
PANEL_PASSWORD = os.getenv("PANEL_PASSWORD")
PANEL_SECRET_KEY = os.getenv("PANEL_SECRET_KEY")