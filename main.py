import logging
from pathlib import Path

import discord
from discord.ext import commands

from src import configure_logging
from src.constants import (
    AppMode,
    COMMAND_FILES,
    VOICE_MESSAGE_IND,
    VOICE_MESSAGE_GIF,
)
from src.settings import get_settings


configure_logging()
logger = logging.getLogger(__name__)

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(
    command_prefix='/',
    intents=intents,
    help_command=commands.DefaultHelpCommand(),
)


@bot.event
async def on_ready():
    """On launch actions"""
    logger.info('Стартуем!')
    settings = get_settings()

    if settings.APP_MODE == AppMode.DEV:
        logger.warning(
            "\n############################################################\n"
            "#                        АХТУНГ!                           #\n"
            "#  Сталкер, внимание! Приложение запущено в DEV окружении  #\n"
            "#             Application is running on DEV mode           #\n"
            "############################################################\n"
        )

    for command_file in (Path(__file__).parent / 'src' / 'commands').glob("*.py"):
        if command_file.name not in COMMAND_FILES:
            continue

        module = f'src.commands.{command_file.name[:-3]}'
        await bot.load_extension(module)

        logger.debug(f'Loaded module {module}')

    logger.info('Initialization complete')
    await bot.change_presence(activity=discord.Game(name='UrAnus'))


@bot.event
async def on_message(message: discord.Message):
    """Every message in channel event"""
    if message.author == bot.user:
        return

    if message.attachments and message.attachments[0].filename == VOICE_MESSAGE_IND:
        await message.reply(VOICE_MESSAGE_GIF)

    await bot.process_commands(message)


if __name__ == '__main__':
    settings = get_settings()

    bot.run(token=settings.TOKEN)
