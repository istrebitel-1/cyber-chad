import asyncio
import logging
from json import JSONDecodeError
from typing import Dict

from discord import File
from discord.player import FFmpegPCMAudio, PCMVolumeTransformer
from discord.ext import commands

from src.commands.constants import VoiceChannelCommands, DEFAULT_TRACK_TITLE, TRACK_TITLE_KEY
from src.commands.utils import is_author_connected_to_voice
from src.services.queue import (
    Queue,
    get_guild_queue,
    run_tracks_queue,
    get_track_info,
)
from src.services.aneki import save_anek, get_anek
from src.settings import get_settings


logger = logging.getLogger(__name__)


@commands.group()
async def voice(ctx: commands.Context):
    if ctx.invoked_subcommand is None:
        await ctx.send(f"No, {ctx.subcommand_passed} does not belong to simple")


tracks_queue: Dict[int, Queue] = {}


@voice.command(
    name=VoiceChannelCommands.JOIN,
    aliases=['j', 'podliva_join', 'get_your_ass_back_here'],
)
async def join_voice_channel(ctx: commands.Context):
    """Join voice channel and says something...

    Args:
        ctx (commands.Context): Discord context
    """
    if not is_author_connected_to_voice(ctx=ctx):
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
    name=VoiceChannelCommands.LEAVE,
    aliases=['podliva_leave', 'fuck_you'],
)
async def leave_voice_channel(ctx: commands.Context):
    """Leave voice channel

    Args:
        ctx (commands.Context): Discord context
    """
    if ctx.voice_client:
        await ctx.guild.voice_client.disconnect()
    else:
        pass


@voice.command(
    name=VoiceChannelCommands.JOKE,
    aliases=['anek'],
)
async def parse_and_play_random_joke(ctx: commands.Context):
    """Get random joke from open API, send to Sber Salut API,
      save it to file and plays in voice channel

    Args:
        ctx (commands.Context): Discord context
    """
    if not is_author_connected_to_voice(ctx=ctx):
        await ctx.send(f'{ctx.author.mention} Подключись к голосовому каналу, сталкер')
        return

    try:
        anek_text = get_anek()
    except JSONDecodeError:
        logger.error('Invalid json received')
        await ctx.reply('Чот анек плохой попался, не покажу. Попробуй еще раз')
        return

    if not (anek_path := save_anek(anek_text)):
        logger.error('Error to save "anek"')
        return

    await ctx.reply(anek_text, file=File(anek_path))

    settings = get_settings()

    channel = ctx.message.author.voice.channel
    voice = ctx.voice_client if ctx.voice_client else await channel.connect()

    source = FFmpegPCMAudio(
        executable=settings.FFMPEG_EXECUTABLE_PATH,
        source=anek_path,
    )
    source = PCMVolumeTransformer(source, volume=2.0)

    voice.play(source)

    while voice.is_playing():
        await asyncio.sleep(1)


@voice.command(
    name=VoiceChannelCommands.PLAY,
    aliases=['p'],
)
async def play_audio_in_voice_channel(ctx: commands.Context, youtube_url: str):
    """Plays youtube audio

    Args:
        ctx (commands.Context): Discord context
        youtube_url (str): Url to yourube video
    """
    if not is_author_connected_to_voice(ctx=ctx):
        await ctx.send(f'{ctx.author.mention} Подключись к голосовому каналу, сталкер')
        return

    voice = ctx.voice_client if ctx.voice_client else await ctx.message.author.voice.channel.connect()
    voice.stop()

    queue_: Queue = get_guild_queue(tracks_queue=tracks_queue, guild_id=ctx.guild.id)

    track_info = get_track_info(url=youtube_url)
    track_title = track_info.get(TRACK_TITLE_KEY, DEFAULT_TRACK_TITLE)

    queue_.clear()
    queue_.append(url=youtube_url, title=track_title)

    await run_tracks_queue(
        ctx=ctx,
        queue_=queue_,
        voice=voice,
    )


@voice.command(
    name=VoiceChannelCommands.QUEUE,
    aliases=['q'],
)
async def queue_track(ctx: commands.Context, youtube_url: str):
    """Add track to queue

    Args:
        ctx (commands.Context): Discord context
        youtube_url (str): Url to yourube video
    """
    queue_: Queue = get_guild_queue(tracks_queue=tracks_queue, guild_id=ctx.guild.id)

    if queue_.is_empty:
        tracks_queue[ctx.guild.id] = queue_

    track_title = get_track_info(url=youtube_url).get(TRACK_TITLE_KEY, DEFAULT_TRACK_TITLE)

    queue_.append(url=youtube_url, title=track_title)

    await ctx.send(f"Добавлен трецк: {track_title}")


@voice.command(
    name=VoiceChannelCommands.CLEAR,
    aliases=['c'],
)
async def clear_tracks_queue(ctx: commands.Context):
    """Clear tracks queue

    Args:
        ctx (commands.Context): Discord context
    """
    queue_: Queue = get_guild_queue(tracks_queue=tracks_queue, guild_id=ctx.guild.id)

    if queue_.is_empty:
        tracks_queue.clear()

    await ctx.send("Очередь очищена")


@voice.command(
    name=VoiceChannelCommands.NEXT,
    aliases=['n', 'skip'],
)
async def play_next_track(ctx: commands.Context, track_num: int | None = None):
    """Plays next track from guild's queue

    Args:
        ctx (commands.Context): Discord context
        track_num (int): Number of track in queue
    """
    if not is_author_connected_to_voice(ctx=ctx):
        await ctx.send(f'{ctx.author.mention} Подключись к голосовому каналу, сталкер')
        return

    voice = ctx.voice_client if ctx.voice_client else await ctx.message.author.voice.channel.connect()
    voice.stop()

    queue_: Queue = get_guild_queue(tracks_queue=tracks_queue, guild_id=ctx.guild.id)

    await run_tracks_queue(
        ctx=ctx,
        queue_=queue_,
        voice=voice,
        start_item=track_num - 1,
    )


@voice.command(
    name=VoiceChannelCommands.LIST,
    aliases=['l'],
)
async def list_guild_track_queue(ctx: commands.Context):
    """List tracks queue

    Args:
        ctx (commands.Context): Discord context
    """
    queue_: Queue = get_guild_queue(tracks_queue=tracks_queue, guild_id=ctx.guild.id)

    await ctx.send(str(queue_))


async def setup(bot: commands.bot.Bot) -> None:
    """Setup function for load commands module

    Args:
        bot (commands.bot.Bot): Discord bot class
    """
    bot.add_command(clear_tracks_queue)
    bot.add_command(join_voice_channel)
    bot.add_command(leave_voice_channel)
    bot.add_command(list_guild_track_queue)
    bot.add_command(play_audio_in_voice_channel)
    bot.add_command(play_next_track)
    bot.add_command(queue_track)
    bot.add_command(parse_and_play_random_joke)
