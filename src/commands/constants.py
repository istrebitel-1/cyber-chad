from src.constants import StringEnumBase
from src.core.utils import get_command_prefix


class YoutubeQualityType(StringEnumBase):
    """Youtube download quality"""
    ULTRALOW = 'ultralow'
    LOW = 'low'
    MEDIUM = 'medium'


class EmojisCommands(StringEnumBase):
    """Base command for Emojis module"""
    EMOJI = f'{get_command_prefix()}emoji'
    REACT = f'{get_command_prefix()}react'


class SynthesizeCommands(StringEnumBase):
    """Base command for Synthesize module"""
    SYNTHESIZE = f'{get_command_prefix()}synthesize'


class TextChannelCommands(StringEnumBase):
    """Base command for `Text channel` module"""
    TRAP = f'{get_command_prefix()}trap'


class VoiceChannelCommands(StringEnumBase):
    """Base command for `Voice channel` module"""
    CLEAR = f'{get_command_prefix()}clear'
    DELETE = f'{get_command_prefix()}delete'
    JOIN = f'{get_command_prefix()}join'
    JOKE = f'{get_command_prefix()}joke'
    LEAVE = f'{get_command_prefix()}leave'
    LIST = f'{get_command_prefix()}list'
    NEXT = f'{get_command_prefix()}next'
    PLAY = f'{get_command_prefix()}play'
    QUEUE = f'{get_command_prefix()}queue'


DEFAULT_TRACK_TITLE = 'Без названия - Неизвестен'
TRACK_TITLE_KEY = 'title'
