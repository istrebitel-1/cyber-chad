import asyncio
import logging

from discord.player import FFmpegPCMAudio, PCMVolumeTransformer
from discord.ext import commands
from discord import File

from src.commands.constants import SynthesizeCommands
from src.services.synthesize import synthesize_text
from src.settings import get_settings


logger = logging.getLogger(__name__)


@commands.group()
async def synthesize(ctx: commands.Context, /):
    if ctx.invoked_subcommand is None:
        await ctx.send(f"No, {ctx.subcommand_passed} does not belong to simple")


@synthesize.command(
    name=SynthesizeCommands.SYNTHESIZE,
    aliases=['s'],
)
async def synthesize_sentence(ctx: commands.Context, text: str, play_to_voice: bool = True, /) -> None:
    """Synthesize speech from text

    Args:
        ctx (commands.Context): Discord context
        text (str): Text to synthesize
        play_to_voice (bool, optional): Plays text to voice channel. Defaults to True.
    """
    if not ctx.author.voice:
        logger.warning(f'{ctx.author.mention} not connected to voice')
        await ctx.send(f'{ctx.author.mention} Подключись к голосовому каналу, сталкер')
        return

    try:
        audio_file = synthesize_text(text=text)
    except Exception as e:
        logger.error(f'{e.__class__}: {str(e)}')
        return None

    await ctx.reply(file=File(audio_file))

    if not play_to_voice:
        return None

    settings = get_settings()

    channel = ctx.message.author.voice.channel
    voice = ctx.voice_client if ctx.voice_client else await channel.connect()
    source = FFmpegPCMAudio(
        executable=str(settings.FFMPEG_EXECUTABLE_PATH),
        source=audio_file,
    )
    source_transformed = PCMVolumeTransformer(source, volume=2.0)

    voice.play(source_transformed)

    while voice.is_playing():
        await asyncio.sleep(1)


def setup(bot: commands.bot.Bot) -> None:
    """Setup function for load commands module

    Args:
        bot (commands.bot.Bot): Discord bot class
    """
    bot.add_command(synthesize_sentence)
