import discord


from resources import bot
from settings import settings


# on launch
@bot.event
async def on_ready():
    print('ok')
    await bot.change_presence(activity=discord.Game(name='UrAnus'))


# run bot
bot.run(settings['token'])
