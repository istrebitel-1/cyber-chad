from datetime import datetime
import logging

from yandex_music import Client

from src.core.exceptions import YandexMusicTokenExpired
from src.constants import AppMode, DEV_COMMAND_PREFIX
from src.settings import get_settings


logger = logging.getLogger(__name__)


def get_command_prefix() -> str:
    """Get commands prefix

    Returns:
        str: Commands prefix
    """
    settings = get_settings()

    return DEV_COMMAND_PREFIX if settings.APP_MODE == AppMode.DEV else ''


def get_yandex_music_api_client() -> Client:
    """Get YM API Client

    Raises:
        YandexMusicTokenExpired: Token has expired

    Returns:
        Client: Client
    """
    settings = get_settings()

    client = Client(token=settings.YANDEX_MUSIC_TOKEN).init()

    if datetime.now() > settings.YANDEX_MUSIC_TOKEN_EXP_DATE:
        raise YandexMusicTokenExpired("Необходимо обновить токен YandexMusic")

    return client
