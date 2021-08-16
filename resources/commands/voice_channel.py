from discord.player import FFmpegPCMAudio
from resources import bot

# join voice channel
@bot.command()
async def podliva_join(ctx):
	if (ctx.author.voice):
		channel = ctx.message.author.voice.channel
		voice = await channel.connect()
		source = FFmpegPCMAudio(
			executable="ffmpeg/ffmpeg.exe", source="audio/nc.mp3")
		player = voice.play(source)


# leave voice channel
@bot.command()
async def podliva_leave(ctx):
	await ctx.guild.voice_client.disconnect()