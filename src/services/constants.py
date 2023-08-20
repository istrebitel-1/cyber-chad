from src.constants import StringEnumBase


class TrackSource(StringEnumBase):
    """Track source"""
    YANDEX_MUSIC = 'yandex_music'
    YOUTUBE = 'youtube'


YDL_OPTIONS = {
    'format': 'bestaudio',
    'noplaylist': True,
    'ignoreerrors': True,
}
FFMPEG_OPTIONS = {
    'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
    'options': '-vn',
}
