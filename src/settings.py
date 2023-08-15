from pathlib import Path

from pydantic import BaseSettings

from src.constants import AppMode


class Settings(BaseSettings):
    """Bot env settings"""
    TOKEN: str

    APP_MODE: AppMode = AppMode.DEV
    FFMPEG_EXECUTABLE_PATH: str | Path = 'ffmpeg/ffmpeg.exe'

    JOKES_URL: str = 'http://rzhunemogu.ru/RandJSON.aspx?CType=1'

    SBER_SALUTE_CLIENT_SECRET: str
    SBER_SALUTE_AUTH_DATA: str


def get_settings() -> Settings:
    """Get app settings"""
    return Settings()
