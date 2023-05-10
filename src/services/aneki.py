import json

import pyttsx3
import requests

from src.settings import get_settings


synthesizer = pyttsx3.init()


def get_anek() -> str:
    settings = get_settings()

    responce = requests.get(settings.JOKES_URL)
    anek = json.loads(responce.text.replace('\r\n', ' '))['content']

    return anek


def save_anek(anek):
    synthesizer = pyttsx3.init()

    synthesizer.save_to_file(anek, 'audio/anek.mp3')
    synthesizer.runAndWait()

    return 'success'
