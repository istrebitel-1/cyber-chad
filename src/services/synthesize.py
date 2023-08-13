import json
import uuid
from typing import Dict

import requests

from src.constants import (
    SBER_TEXT_SYNTHESIZE_API_URL,
    SBER_SALUTE_API_URL,
    SBER_SERVICE_NAME
)
from src.settings import get_settings


def synthesize_text(text: str) -> str:
    """Synthesize opus file from given text"""
    settings = get_settings()

    request_uuid = str(uuid.uuid4())

    session = requests.Session()

    response = session.post(
        url=SBER_SALUTE_API_URL,
        headers={
            'Authorization': f'Basic {settings.SBER_SALUTE_AUTH_DATA}',
            'RqUID': request_uuid,
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        verify='russian_trusted_root_ca.cer',
        data={
            'scope': SBER_SERVICE_NAME,
        }
    )

    token_data: Dict = json.loads(response.text)

    auth_headers = {
        'Authorization': f'Bearer {token_data.get("access_token")}'
    }

    data = session.post(
        url=SBER_TEXT_SYNTHESIZE_API_URL,
        headers={
            'Content-Type': 'application/text',
            **auth_headers,
        },
        data=text.encode(),
        verify='russian_trusted_root_ca.cer',
    )

    file_name = f'audio/{request_uuid}.opus'

    with open(file_name, 'wb') as f:
        f.write(data.content)

    return file_name
