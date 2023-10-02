import asyncio
import logging
from typing import Dict

import discord
from discord.ext import commands

from src.commands.constants import CompanionCompletionCommands
from src.commands.utils import is_author_connected_to_voice
from src.services.completion import generate
from src.services.recognize import recognize_audio
from src.services.synthesize import synthesize_text
from src.settings import get_settings


logger = logging.getLogger(__name__)

connections: Dict[int, discord.VoiceClient] = {}


@commands.group(name='talk')
async def completion_group(ctx: commands.Context, /):
    if ctx.invoked_subcommand is None:
        await ctx.send(f"No, {ctx.subcommand_passed} does not belong to simple")


async def record_finish_callback(
        sink: discord.sinks.MP3Sink,
        channel: discord.TextChannel,
        *args,
) -> None:
    """Callback on record stop

    Args:
        sink (discord.sinks.MP3Sink): pycord sink class
        channel (discord.TextChannel): text channel
    """
    for user_id, audio in sink.audio_data.items():
        transcription = await recognize_audio(audio.file)
        result = await generate(prompt=transcription)

        try:
            audio_file = synthesize_text(text=result)
        except Exception as e:
            logger.error(f'{e.__class__}: {str(e)}')
            return None

        settings = get_settings()

        source = discord.FFmpegPCMAudio(
            executable=settings.FFMPEG_EXECUTABLE_PATH,
            source=audio_file,
        )
        source = discord.PCMVolumeTransformer(source, volume=2.0)

        # sink.vc is actually discord.VoiceClient
        sink.vc.play(source)  # type: ignore

        while sink.vc.is_playing():  # type: ignore
            await asyncio.sleep(1)

        await channel.send(
            f"{user_id}.{sink.encoding}: {result}",
            file=discord.File(audio_file),
        )


@completion_group.command(
    name=CompanionCompletionCommands.ASK,
    aliases=['talk'],
)
async def completion(ctx: commands.Context, recieve_time: int | None = None, /) -> None:
    """Listen to voice channel and answer to it

    Args:
        ctx (commands.Context): Discord context
        recieve_time (int | None, optional): Time to record. Defaults to None.
    """
    if not await is_author_connected_to_voice(ctx=ctx):
        return None

    voice = ctx.voice_client if ctx.voice_client else await ctx.message.author.voice.channel.connect()

    connections.update({ctx.guild.id: voice})

    if not voice.is_connected():
        await voice.connect()

    voice.start_recording(
        discord.sinks.MP3Sink(),
        record_finish_callback,
        ctx.channel,
    )

    await asyncio.sleep(recieve_time or 10)

    if voice.recording:
        voice.stop_recording()

    await ctx.send('Всё, я больше вас не слушаю')


def setup(bot: commands.bot.Bot) -> None:
    """Setup function for load commands module

    Args:
        bot (commands.bot.Bot): Discord bot class
    """
    bot.add_command(completion)
