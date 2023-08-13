import json
from typing import Optional

import requests

from src.services.synthesize import synthesize_text
from src.settings import get_settings


def get_anek() -> str:
    settings = get_settings()

    responce = requests.get(settings.JOKES_URL)
    anek = json.loads(responce.text.replace('\r\n', ' '))['content']

    return anek


def save_anek(anek: str) -> Optional[str]:
    try:
        return synthesize_text(text=anek)
    except Exception:
        return None
