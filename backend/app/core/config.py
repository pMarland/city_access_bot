import os
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """
    Основные настройки приложения.
    Читаются из переменных окружения или .env файла.
    """
    
    # --- Database ---
    DATABASE_URL: str = "postgresql+psycopg2://geobot:geobot@db:5432/geobot"

    # --- Telegram Bot ---
    TELEGRAM_BOT_TOKEN: str = os.getenv("TELEGRAM_BOT_TOKEN", "")

    # --- Media files ---
    MEDIA_DIR: str = os.getenv("MEDIA_DIR", "media")  # Папка для хранения файлов

    # --- GIS / spatial ---
    DEFAULT_SRID: int = 4326  # используемый SRID для геоданных

    # --- FastAPI / debug ---
    DEBUG: bool = True

    class Config:
        env_file = ".env"  # читаем переменные окружения из файла .env
        env_file_encoding = "utf-8"

# Создаем глобальный объект настроек
settings = Settings()
