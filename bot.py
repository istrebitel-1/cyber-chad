
import discord

from resources import bot
from settings import settings


@bot.event
async def on_ready():
    """On launch actions"""
    await bot.change_presence(activity=discord.Game(name='UrAnus'))


if __name__ == '__main__':
    bot.run(settings['token'])
