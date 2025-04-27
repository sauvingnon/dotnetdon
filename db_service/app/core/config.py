# app/core/config.py

from dotenv import load_dotenv
from pydantic_settings import BaseSettings
import os

class Settings(BaseSettings):
    DATABASE_URL: str
    postgres_db: str
    postgres_user: str
    postgres_password: str

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()