from pydantic import BaseSettings


class Settings(BaseSettings):
    """Bot env settings"""
    token: str


def get_settings() -> Settings:
    """Get app settings"""
    return Settings()
