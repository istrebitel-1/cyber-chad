from src.constants import AppMode, DEV_COMMAND_PREFIX
from src.settings import get_settings


def get_command_prefix() -> str:
    """Get commands prefix

    Returns:
        str: Commands prefix
    """
    settings = get_settings()

    return DEV_COMMAND_PREFIX if settings.APP_MODE == AppMode.DEV else ''
