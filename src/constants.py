from enum import Enum


class StringEnumBase(str, Enum):
    """Base Enum class for str type"""
    def __str__(self):
        return self.value


class AppMode(StringEnumBase):
    """Application mode"""
    DEV = 'DEV'
    PROD = 'PROD'


COMMAND_FILES = (
    'emojis.py',
    'synthesize.py',
    'text_channel.py',
    'voice_channel.py',
)

DEV_COMMAND_PREFIX = 'dev_'

VOICE_MESSAGE_IND = 'voice-message.ogg'
VOICE_MESSAGE_GIF = 'https://media.tenor.com/tBv6AL0fyzwAAAAC/getting-spanked-spank.gif'

GIGACHADS_GUILD_ID = 715666531802939393

SBER_SALUTE_API_URL = 'https://ngw.devices.sberbank.ru:9443/api/v2/oauth'
SBER_TEXT_SYNTHESIZE_API_URL = 'https://smartspeech.sber.ru/rest/v1/text:synthesize'
SBER_SERVICE_NAME = 'SALUTE_SPEECH_PERS'
