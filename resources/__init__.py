from settings import settings
from discord.ext import commands


# define bot
bot = commands.Bot(command_prefix=settings['prefix'])


# import all commands
import resources.commands
