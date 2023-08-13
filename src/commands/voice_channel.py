import asyncio
import logging
from typing import Dict, Optional

import yt_dlp as youtube_dl
from discord.player import FFmpegPCMAudio
from discord.ext import commands

from src.services.aneki import save_anek, get_anek
from src.settings import get_settings


logger = logging.getLogger(__name__)


@commands.group()
async def voice(ctx: commands.Context):
    if ctx.invoked_subcommand is None:
        await ctx.send(f"No, {ctx.subcommand_passed} does not belong to simple")


class Queue:
    """Очередь трецков"""
    def __init__(self) -> None:
        self.tracks_url = []

    @property
    def is_empty(self) -> bool:
        return self.tracks_url == []

    def append(self, url) -> None:
        """Добавление трека в куеуе"""
        self.tracks_url.append(url)

    def pop(self) -> str | None:
        """попит левый трецк"""
        return self.tracks_url.pop(0) if self.tracks_url else None

    def clear(self) -> None:
        """Очищает очередб"""
        self.tracks_url = []


def get_guild_queue(guild_id: int) -> Queue:
    """Получение голосового канала"""
    queue_: Queue = tracks_queue.get(guild_id) or Queue()

    if queue_.is_empty:
        tracks_queue[guild_id] = queue_

    return queue_


tracks_queue: Dict[str, Queue] = {}


@voice.command(
    name='podliva_join',
    aliases=['join', 'get_your_ass_back_here'],
)
async def join(ctx: commands.Context):
    """Join voice channel and says 'nice c**k''"""
    if not ctx.author.voice:
        logger.warning(f'{ctx.author.mention} not connected to voice')
        await ctx.send(f'{ctx.author.mention} Подключись к голосовому каналу, сталкер')
        return

    settings = get_settings()
    channel = ctx.message.author.voice.channel
    voice = ctx.voice_client if ctx.voice_client else await channel.connect()

    source = FFmpegPCMAudio(
        executable=settings.FFMPEG_EXECUTABLE_PATH,
        source="audio/nc.mp3",
    )
    voice.play(source)


@voice.command(
    name='podliva_leave',
    aliases=['leave', 'fuck_you'],
)
async def leave(ctx: commands.Context):
    """Leave voice channel"""
    if ctx.voice_client:
        await ctx.guild.voice_client.disconnect()
    else:
        pass


@voice.command(
    name='say',
    aliases=['anek'],
)
async def say(ctx: commands.Context):
    """Say anek from mp3 file"""
    if not ctx.author.voice:
        logger.warning(f'{ctx.author.mention} not connected to voice')
        await ctx.send(f'{ctx.author.mention} Подключись к голосовому каналу, сталкер')
        return

    if not (anek_path := save_anek(get_anek())):
        logger.error('Error to save "anek"')
        return

    settings = get_settings()

    channel = ctx.message.author.voice.channel
    voice = ctx.voice_client if ctx.voice_client else await channel.connect()
    source = FFmpegPCMAudio(
        executable=settings.FFMPEG_EXECUTABLE_PATH,
        source=anek_path,
    )

    voice.play(source)

    while voice.is_playing():
        await asyncio.sleep(1)


@voice.command(
    name='play',
    aliases=['p'],
)
async def play(ctx: commands.Context, youtube_url: str):
    """Plays youtube audio"""
    YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist': 'False'}
    FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}

    settings = get_settings()

    if not ctx.author.voice:
        logger.warning(f'{ctx.author.mention} not connected to voice')
        await ctx.send(f'{ctx.author.mention} Подключись к голосовому каналу, сталкер')
        return

    voice = ctx.voice_client if ctx.voice_client else await ctx.message.author.voice.channel.connect()
    voice.stop()

    queue_ = get_guild_queue(ctx.guild.id)
    queue_.clear()
    queue_.append(youtube_url)

    while True:
        if not (url := get_guild_queue(ctx.guild.id).pop()):
            break

        with youtube_dl.YoutubeDL(YDL_OPTIONS) as ydl:
            info = ydl.extract_info(url, download=False)

        # TODO: enum
        allowed_quality = ('ultralow', 'low', 'medium')
        try:
            audio: Optional[str] = None
            for format_ in info['formats']:
                if isinstance(format_, dict) and \
                        format_.get('format_note') in allowed_quality:
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

        voice.play(FFmpegPCMAudio(
            source=audio,
            executable=settings.FFMPEG_EXECUTABLE_PATH,
            **FFMPEG_OPTIONS,
        ))

        while voice.is_playing():
            await asyncio.sleep(1)

    await ctx.send('Очередь треков завершилась, я пошёл отдыхать')


@voice.command(
    name='queye',
    aliases=['куеуе', 'q'],
)
async def queue(ctx: commands.Context, youtube_url: str):
    """Add track to queue"""
    queue_: Queue | None = tracks_queue.get(ctx.guild.id) or Queue()

    if not queue_:
        tracks_queue[ctx.guild.id] = queue_

    queue_.clear()
    queue_.append(youtube_url)

    await ctx.send("Добавлен трецк флек$$овый")


@voice.command(
    name='clear',
)
async def clear(ctx: commands.Context):
    """Clear tracks queue"""
    queue_: Queue | None = tracks_queue.get(ctx.guild.id) or Queue()

    if not queue_:
        tracks_queue[ctx.guild.id] = queue_

    await ctx.send("Очередь очищена")


async def setup(bot: commands.bot.Bot):
    bot.add_command(voice)
    bot.add_command(join)
    bot.add_command(leave)
    bot.add_command(say)
    bot.add_command(play)
    bot.add_command(queue)
    bot.add_command(clear)
