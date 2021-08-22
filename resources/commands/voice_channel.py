from discord.player import FFmpegPCMAudio
from resources import bot

# join voice channel
@bot.command(
    name='podliva_join',
    aliases=['join', 'get your ass back here']
)
async def join(ctx):
    if (ctx.author.voice):
        channel = ctx.message.author.voice.channel
        voice = await channel.connect()
        source = FFmpegPCMAudio(
            executable="ffmpeg/ffmpeg.exe", source="audio/nc.mp3")
        player = voice.play(source)


# leave voice channel
@bot.command(
    name='podliva_leave',
    aliases=['leave', 'fuck you']
)
async def leave(ctx):
    await ctx.guild.voice_client.disconnect()
