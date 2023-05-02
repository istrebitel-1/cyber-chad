import logging
from pathlib import Path

import discord
from discord.ext import commands

from src import configure_logging
from src.constants import VOICE_MESSAGE_IND, VOICE_MESSAGE_GIF
from src.settings import get_settings


configure_logging()
logger = logging.getLogger(__name__)

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='/', intents=intents)


@bot.event
async def on_ready():
    """On launch actions"""
    logger.info('Стартуем!')

    for cmd_file in (Path(__file__).parent / 'src' / 'commands').glob("*.py"):
        if cmd_file.name == '__init__.py':
            continue

        module = f'src.commands.{cmd_file.name[:-3]}'
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
    elif message.content.lower() == 'да':
        await message.reply('pizda')
    elif message.content.lower() == 'нет':
        await message.reply('pidora otvet')

    await bot.process_commands(message)


if __name__ == '__main__':
    settings = get_settings()

    bot.run(token=settings.token)
