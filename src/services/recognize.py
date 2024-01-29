from io import BytesIO
import json
import uuid
from typing import Dict


import requests

from src.constants import (
    SBER_SPEECH_RECOGNIZE_API_URL,
    SBER_AUTH_API_URL,
    SBER_SALUTE_SCOPE
)
from src.settings import get_settings


async def recognize_audio(file: BytesIO) -> str:
    """Recognize Audio file to text

    Args:
        file (BytesIO): audio file

    Returns:
        str: file transcription
    """
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

    data = session.post(
        url=SBER_SPEECH_RECOGNIZE_API_URL,
        headers={
            'Content-Type': 'audio/mpeg;bit=128;rate=48000',
            **auth_headers,
        },
        data=file,
        verify='russian_trusted_root_ca.cer',
    )

    return ' '.join(data.json().get('result'))
