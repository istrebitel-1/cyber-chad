import discord
from discord import channel
from discord.ext import commands
from discord.player import FFmpegPCMAudio

from settings import settings
import asyncio

bot = commands.Bot(command_prefix = settings['prefix'])


# launch bot
@bot.event
async def on_ready():
	await bot.change_presence(activity=discord.Game(name='UrAnus'))


@bot.command()
async def test(ctx, arg):
	await ctx.send(arg)


@bot.command()
async def podliva_join(ctx):
	if (ctx.author.voice):
		channel = ctx.message.author.voice.channel
		voice = await channel.connect()
		source = FFmpegPCMAudio(executable="ffmpeg/ffmpeg.exe", source="audio/kek.mp3")
		player = voice.play(source)
		podliva_leave(ctx)


@bot.command()
async def podliva_leave(ctx):
	await ctx.guild.voice_client.disconnect()


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
	

bot.run(settings['token']) 
