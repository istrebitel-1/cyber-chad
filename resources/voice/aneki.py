import json
import re

import pyttsx3
import requests
import bs4

from requests.api import get


synthesizer = pyttsx3.init()


def get_anek():
    responce = requests.get('http://rzhunemogu.ru/RandJSON.aspx?CType=1')
    soup = bs4.BeautifulSoup(responce.text, 'html.parser')

    return re.sub('[\r\n\{\}"]', '', soup).split(':')[1]


def save_anek(anek):
    synthesizer = pyttsx3.init()

    synthesizer.save_to_file(anek, 'audio/anek.mp3')
    synthesizer.runAndWait()

    return 'success'
