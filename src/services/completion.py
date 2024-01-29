import json
import logging
import uuid

import openai
import requests

from src.constants import SBER_GIGACHAT_API_URL, SBER_AUTH_API_URL, SBER_GIGACHAT_SCOPE, CompletionModel
from src.settings import get_settings


logger = logging.getLogger(__name__)


async def generate(prompt: str) -> str:
    """Generate response from openAI llm

    Args:
        prompt (str): input prompt

    Returns:
        str: LLM response
    """
    logger.info(f' User prompt: {prompt}')
    settings = get_settings()

    if settings.COMPLETION_MODEL == CompletionModel.OPENAI:
        openai.api_key = settings.OPENAI_TOKEN

        chat = openai.ChatCompletion(
            model='gpt-3.5-turbo',
            temperature=0,
            verbose=True,
            max_retries=3,
            request_timeout=60,
        )

        response = await chat.acreate(
            model="gpt-3.5-turbo", messages=[{'role': 'user', 'content': prompt}]
        )
        result = response.choices[0].message.content

        return result

    if settings.COMPLETION_MODEL == CompletionModel.GIGACHAT:
        request_uuid = str(uuid.uuid4())

        session = requests.Session()

        response = session.post(
            url=SBER_AUTH_API_URL,
            headers={
                'Authorization': f'Basic {settings.SBER_GIGACHAT_TOKEN}',
                'RqUID': request_uuid,
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            verify='russian_trusted_root_ca.cer',
            data={
                'scope': SBER_GIGACHAT_SCOPE,
            }
        )

        token_data: dict = json.loads(response.text)

        auth_headers = {
            'Authorization': f'Bearer {token_data.get("access_token")}'
        }

        response = session.post(
            url=SBER_GIGACHAT_API_URL,
            headers=auth_headers,
            verify='russian_trusted_root_ca.cer',
            json={
                'model': 'GigaChat:latest',
                'messages': [
                    {
                        'role': 'user',
                        'content': prompt,
                    }
                ]
            }
        )

        return response.json()['choices'][0]['message']['content']

    assert False, f'No completion model {settings.COMPLETION_MODEL} found'
