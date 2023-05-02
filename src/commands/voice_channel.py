import logging
from typing import Dict

import yt_dlp as youtube_dl
from discord.player import FFmpegPCMAudio
from discord.ext import commands

from src.voice.aneki import save_anek, get_anek


logger = logging.getLogger(__name__)


@commands.group()
async def voice(ctx: commands.Context):
    if ctx.invoked_subcommand is None:
        await ctx.send(f"No, {ctx.subcommand_passed} does not belong to simple")


class Queue:
    """Очередь трецков"""
    def __init__(self) -> None:
        self.tracks_url = []

    def append_track(self, url):
        """Добавление трека в куеуе"""
        self.tracks_url.append(url)

    def pop_track(self):
        """попит левый трецк"""
        self.tracks_url.pop(0)

    def clear_queue(self):
        """Очищает очередб"""
        self.tracks_url = []


tracks_queue: Dict[str, Queue] = {}


@voice.command(
    name='podliva_join',
    aliases=['join', 'get_your_ass_back_here'],
)
async def join(ctx: commands.Context):
    """Join voice channel and says 'nice c**k''"""
    if ctx.author.voice:
        channel = ctx.message.author.voice.channel
        voice = await channel.connect()
        source = FFmpegPCMAudio(
            executable="ffmpeg/ffmpeg.exe",
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
    if ctx.author.voice:
        if save_anek(get_anek()) == 'success':
            channel = ctx.message.author.voice.channel
            voice = await channel.connect()
            source = FFmpegPCMAudio(
                executable="ffmpeg/ffmpeg.exe",
                source="audio/anek.mp3",
            )
            voice.play(source)

            await ctx.guild.voice_client.disconnect()


@voice.command(
    name='play',
    aliases=['p'],
)
async def play(ctx: commands.Context, youtube_url: str, quality: str = 'ultralow'):
    """Plays youtube audio"""
    YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist': 'False'}
    FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
    if ctx.author.voice:
        channel = ctx.message.author.voice.channel

        try:
            voice = await channel.connect()
        except Exception:
            voice = channel

        queue_ = tracks_queue.get(ctx.guild.id)
        if not queue_:
            tracks_queue[ctx.guild.id] = []

        queue_.clear_queue()
        queue_.append_track(youtube_url)

        for url in queue_.tracks_url:
            with youtube_dl.YoutubeDL(YDL_OPTIONS) as ydl:
                info = ydl.extract_info(url, download=False)

            # TODO: enum (ultralow, low, medium)
            try:
                for format_ in info['formats']:
                    if format_['format_note'] == quality:
                        audio = format_['url']

                if not audio:
                    logger.warning(f'Не найдено качество {quality}')
                    voice.disconnect()
                    ctx.send(f'Не найдено качество {quality}')
                    return
            except Exception as e:
                logger.error(e)
                voice.disconnect()
                return

            voice.play(FFmpegPCMAudio(
                source=audio,
                executable="ffmpeg/ffmpeg.exe",
                **FFMPEG_OPTIONS
            ))
            voice.is_playing()
            tracks_queue.pop_track()

    else:
        await ctx.send("Already playing song")
        return


@voice.command(
    name='queye',
    aliases=['куеуе', 'q'],
)
async def queue(ctx: commands.Context, url):
    """Add track to queue"""
    tracks_queue.append_track(url)
    await ctx.send("Добавлен трецк флек$$овый")


@voice.command(
    name='clear',
)
async def clear(ctx: commands.Context):
    """Clear tracks queue"""
    tracks_queue.clear_queue()
    await ctx.send("Очередь очищена")


async def setup(bot: commands.bot.Bot):
    bot.add_command(voice)
    bot.add_command(join)
    bot.add_command(leave)
    bot.add_command(say)
    bot.add_command(play)
    bot.add_command(queue)
    bot.add_command(clear)
