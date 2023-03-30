from settings import settings
from discord.ext import commands

bot = commands.Bot(command_prefix=settings['prefix'])
