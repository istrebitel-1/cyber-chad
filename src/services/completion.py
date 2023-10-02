import openai

from src.settings import get_settings


async def generate(prompt: str) -> str:
    """Generate response from openAI llm

    Args:
        prompt (str): input prompt

    Returns:
        str: LLM response
    """
    settings = get_settings()

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
