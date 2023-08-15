import asyncio
import logging
from typing import Dict, List, Optional

import yt_dlp as youtube_dl  # type: ignore
from discord import VoiceClient
from discord.player import FFmpegPCMAudio, PCMVolumeTransformer
from discord.ext import commands

from src.commands.constants import (
    YoutubeQualityType,
    YDL_OPTIONS,
    FFMPEG_OPTIONS,
)
from src.services.dataclasses import TrackInfo
from src.settings import get_settings


logger = logging.getLogger(__name__)


class Queue:
    """Track queue"""
    def __init__(self) -> None:
        self.tracks_info: List[TrackInfo] = []

    def __str__(self) -> str:
        tracks_str = ''.join([f'{i + 1}. {track.title}\n' for i, track in enumerate(self.tracks_info)])

        return f'```Playing next:\n\n{tracks_str}\n```'

    @property
    def is_empty(self) -> bool:
        """Is queue empty"""
        return self.tracks_info == []

    def append(self, url: str, title: str) -> None:
        """Add track to queue"""
        self.tracks_info.append(
            TrackInfo(
                url=url,
                title=title,
            )
        )

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


def get_track_info(url: str, process: bool = False) -> Dict:
    """Gets youtube video info

    Args:
        url (str): youtube url

    Returns:
        Dict: Video info
    """
    info = None

    with youtube_dl.YoutubeDL(YDL_OPTIONS) as ydl:
        info = ydl.extract_info(url, download=False, process=process)

    if isinstance(info, dict):
        return info

    # TODO: Raise
    return {}


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

        info = get_track_info(url=track.url)

        try:
            audio: Optional[str] = None
            for format_ in info['formats']:
                if isinstance(format_, dict) and \
                        format_.get('format_note') in list(YoutubeQualityType):
                    audio = format_['url']
                    break

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
