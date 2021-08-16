import discord
from discord import channel
from discord.ext import commands
from discord.player import FFmpegPCMAudio

from settings import settings
import asyncio

bot = commands.Bot(command_prefix = settings['prefix'])


# on launch
@bot.event
async def on_ready():
	print('ok')
	await bot.change_presence(activity=discord.Game(name='UrAnus'))


# join voice channel
@bot.command()
async def podliva_join(ctx):
	if (ctx.author.voice):
		channel = ctx.message.author.voice.channel
		voice = await channel.connect()
		source = FFmpegPCMAudio(executable="ffmpeg/ffmpeg.exe", source="audio/kek.mp3")
		player = voice.play(source)
		podliva_leave(ctx)


# send PETTHEPEEPO
@bot.command()
async def emojis(ctx):
	print(ctx.guild.emojis)
	await ctx.send('<a:PETTHEPEEPO:749651053288357979>')


# leave voice channel
@bot.command()
async def podliva_leave(ctx):
	await ctx.guild.voice_client.disconnect()


# help ??
@bot.command()
async def podliva_help(ctx):
	await ctx.send('какая помощь, я podliva')


# message in channel event
@bot.event
async def on_message(message):
	if message.author == bot.user:
		return

	if message.content.lower() == 'да':
		await message.channel.send('pizda')
	elif message.content.lower() == 'нет':
		await message.channel.send('pidora otvet')

	await bot.process_commands(message)


# run bot
bot.run(settings['token']) 
