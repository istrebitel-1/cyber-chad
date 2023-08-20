import asyncio
import logging
from typing import Dict, List, Optional

import yt_dlp as youtube_dl  # type: ignore
from discord import VoiceClient
from discord.player import FFmpegPCMAudio, PCMVolumeTransformer
from discord.ext import commands

from src.core.utils import get_yandex_music_api_client
from src.commands.constants import YoutubeQualityType, DEFAULT_TRACK_TITLE, TRACK_TITLE_KEY
from src.services.constants import (
    TrackSource,
    YDL_OPTIONS,
    FFMPEG_OPTIONS,
)
from src.services.dataclasses import TrackInfo
from src.services.track_info import track_source_parser
from src.settings import get_settings

logger = logging.getLogger(__name__)


class Queue:
    """Track queue"""
    def __init__(self) -> None:
        self.tracks_info: List[TrackInfo] = []

    def __str__(self) -> str:
        if not self.tracks_info:
            return 'Нету трецков в очереди, сталкер...'

        tracks_str = ''.join([
            f'{i + 1}. {track.title} [{track.source}]\n'
            for i, track in enumerate(self.tracks_info)
        ])

        return f'```Далее в очереди:\n\n{tracks_str}\n```'

    @property
    def is_empty(self) -> bool:
        """Is queue empty"""
        return self.tracks_info == []

    def append(self, track_info: TrackInfo) -> None:
        """Add track to queue"""
        self.tracks_info.append(track_info)

    def pop(self, item: int) -> TrackInfo | None:
        """Pop track from queue"""
        return self.tracks_info.pop(item) if self.tracks_info else None

    def clear(self) -> None:
        """Clear queue"""
        self.tracks_info = []


def get_guild_queue(tracks_queue: Dict[int, Queue], guild_id: int) -> Queue:
    """Get guild tracks queue

    Args:
        tracks_queue (Dict[str, Queue]): Current track queue
        guild_id (int): Discord guild ID

    Returns:
        Queue: Guild track queue
    """
    queue_: Queue = tracks_queue.get(guild_id) or Queue()

    if queue_.is_empty:
        tracks_queue[guild_id] = queue_

    return queue_


def get_track_info(
        url: str,
        download: bool | None = None,
        process: bool | None = None,
) -> TrackInfo:
    """Gets track info

    Args:
        url (str): youtube url

    Returns:
        TrackInfo: Track info
    """
    if not download:
        download = False

    if not process:
        process = False

    # TODO: Разбить парсер по методам или классам
    match track_source_parser(track_url=url):
        case TrackSource.YANDEX_MUSIC:
            client = get_yandex_music_api_client()

            track_id = int(url.split('/')[-1])
            info = client.tracks(track_id)[0]

            return TrackInfo(
                url=url,
                title=f'{", ".join(info.artists_name())} - {info.title}',
                source=TrackSource.YANDEX_MUSIC,
                extra=info.to_dict(),
            )

        case TrackSource.YOUTUBE:
            with youtube_dl.YoutubeDL(YDL_OPTIONS) as ydl:
                info = ydl.extract_info(url, download=False, process=process)

            if isinstance(info, dict):
                return TrackInfo(
                    url=url,
                    title=info.get(TRACK_TITLE_KEY, DEFAULT_TRACK_TITLE),
                    source=TrackSource.YOUTUBE,
                    extra=info,
                )


async def run_tracks_queue(
        ctx: commands.Context,
        queue_: Queue,
        voice: VoiceClient,
        start_item: int | None = None,
) -> None:
    """Run tracks from queue

    Args:
        ctx (commands.Context): Discord context
        queue_ (Queue): Guild tracks queue
        voice (VoiceClient): Discord voice client
        start_item (int, optional): Start queue item. Defaults to 0.
    """

    settings = get_settings()

    while True:
        logger.info(f'Guild {ctx.guild.id} queue: {str(queue_)}')

        if not start_item:
            start_item = 0

        if not (track := queue_.pop(start_item)):
            break

        try:
            audio: Optional[str] = None

            # TODO: отдельный метод
            if track.source == TrackSource.YOUTUBE:
                for format_ in track.extra['formats']:
                    if isinstance(format_, dict) and \
                            format_.get('format_note') in list(YoutubeQualityType):
                        audio = format_['url']
                        break
            elif track.source == TrackSource.YANDEX_MUSIC:
                # TODO: кринж полнейший, полностью переделать
                track_id = track.extra['real_id']

                client = get_yandex_music_api_client()

                audio = client.tracks(track_id)[0].get_download_info()[0].get_direct_link()

            if not audio:
                warning_message = 'Не найден контекст для воспроизведения дорожки'
                logger.warning(warning_message)
                await ctx.send(warning_message)
                return
        except Exception as e:
            logger.error(e)
            return

        source = FFmpegPCMAudio(
            source=audio,
            executable=settings.FFMPEG_EXECUTABLE_PATH,
            **FFMPEG_OPTIONS,
        )
        source = PCMVolumeTransformer(source, volume=0.6)

        voice.play(source)

        while voice.is_playing():
            await asyncio.sleep(1)

    await ctx.send('Очередь треков завершилась, я пошёл отдыхать')

    return None
