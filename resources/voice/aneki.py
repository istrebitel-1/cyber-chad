import re

import pyttsx3
import requests
import bs4
from gtts import gTTS


synthesizer = pyttsx3.init()


def get_anek():
    responce = requests.get('http://rzhunemogu.ru/RandJSON.aspx?CType=1')
    soup = bs4.BeautifulSoup(responce.text, 'html.parser')

    return re.sub('[\r\n\{\}"]', '', soup).split(':')[1]


def save_anek(anek):
    myobj = gTTS(text=anek, lang='ru', slow=False)
    myobj.save('audio/anek.mp3')


    return 'success'
