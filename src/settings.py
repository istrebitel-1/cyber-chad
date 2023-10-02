from datetime import datetime
from pathlib import Path

from pydantic import BaseSettings, AnyHttpUrl

from src.constants import AppMode


class Settings(BaseSettings):
    """Bot env settings"""
    DISCORD_BOT_TOKEN: str

    APP_MODE: AppMode = AppMode.DEV
    FFMPEG_EXECUTABLE_PATH: str | Path = 'ffmpeg/ffmpeg.exe'

    JOKES_URL: AnyHttpUrl = 'http://rzhunemogu.ru/RandJSON.aspx?CType=1'

    SBER_SALUTE_CLIENT_SECRET: str
    SBER_SALUTE_AUTH_DATA: str

    YANDEX_MUSIC_TOKEN: str
    YANDEX_MUSIC_TOKEN_EXP_DATE: datetime = datetime(2024, 8, 15)

    OPENAI_TOKEN: str


def get_settings() -> Settings:
    """Get app settings"""
    return Settings()
