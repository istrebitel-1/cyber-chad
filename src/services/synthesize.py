import json
import uuid
from typing import Dict

import requests

from src.constants import (
    SBER_TEXT_SYNTHESIZE_API_URL,
    SBER_AUTH_API_URL,
    SBER_SALUTE_SCOPE
)
from src.settings import get_settings


def synthesize_text(text: str, loudness: str = "x-high") -> str:
    """Synthesize opus file from given text"""
    settings = get_settings()

    request_uuid = str(uuid.uuid4())

    session = requests.Session()

    response = session.post(
        url=SBER_AUTH_API_URL,
        headers={
            'Authorization': f'Basic {settings.SBER_SALUTE_AUTH_DATA}',
            'RqUID': request_uuid,
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        verify='russian_trusted_root_ca.cer',
        data={
            'scope': SBER_SALUTE_SCOPE,
        }
    )

    token_data: Dict = json.loads(response.text)

    auth_headers = {
        'Authorization': f'Bearer {token_data.get("access_token")}'
    }

    ssml_text = f'<speak><paint loudness="{loudness}">{text}</paint></speak>'

    data = session.post(
        url=SBER_TEXT_SYNTHESIZE_API_URL,
        headers={
            'Content-Type': 'application/ssml',
            **auth_headers,
        },
        data=ssml_text.encode(),
        verify='russian_trusted_root_ca.cer',
    )

    file_name = f'audio/{request_uuid}.opus'

    with open(file_name, 'wb') as f:
        f.write(data.content)

    return file_name
