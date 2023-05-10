from pathlib import Path

from pydantic import BaseSettings


class Settings(BaseSettings):
    """Bot env settings"""
    TOKEN: str

    FFMPEG_EXECUTABLE_PATH: str | Path = 'ffmpeg/ffmpeg.exe'

    JOKES_URL: str = 'http://rzhunemogu.ru/RandJSON.aspx?CType=1'
    JOKES_SAVE_PATH: str | Path = 'audio/anek.mp3'


def get_settings() -> Settings:
    """Get app settings"""
    return Settings()
