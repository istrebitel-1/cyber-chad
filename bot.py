import discord
from discord.ext import commands

from settings import settings


bot = commands.Bot(command_prefix = settings['prefix'])


@bot.event
async def on_ready():
	await bot.change_presence(activity=discord.Game(name='UrAnus'))


@bot.event
async def on_message(msg):
	print(msg)


@bot.command()
async def test(ctx):
	ctx.send('ass')


@bot.event
async def on_message(message):
	if message.author == bot.user:
		return

	await message.channel.send('kek')


bot.run(settings['token']) 
