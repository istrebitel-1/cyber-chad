import pyttsx3, requests, bs4
from requests.api import get

synthesizer = pyttsx3.init()

def get_anek():
    anek = ''
    responce = requests.get('http://anekdotme.ru/random')
    soup = bs4.BeautifulSoup(responce.text, 'html.parser')
    anek_item = soup.select('.anekdot_text')

    for item in anek_item:        
        responce = (item.getText().strip())
        anek = anek + responce + '\n\n'

    return responce


def save_anek(anek):
    synthesizer = pyttsx3.init()

    synthesizer.save_to_file(anek, 'audio/anek.mp3')
    synthesizer.runAndWait()

    return 'success'
