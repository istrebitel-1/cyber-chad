from settings import settings
from discord.ext import commands


# define bot
bot = commands.Bot(command_prefix=settings['prefix'])


# import all commands
from resources.commands import (
	podliva_leave, 
	podliva_join, 
	test, 
	on_message, 
	podliva_help, 
	react,
	emojis
)
