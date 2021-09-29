from discord.player import FFmpegPCMAudio
from resources import bot
from resources.voice import save_anek, get_anek


# join voice channel
@bot.command(
    name='podliva_join',
    aliases=['join', 'get_your_ass_back_here']
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
    aliases=['leave', 'fuck_you']
)
async def leave(ctx):
    if (ctx.voice_client):
        await ctx.guild.voice_client.disconnect()
    else:
        pass


# say smth
@bot.command(
    name='say',
    aliases=['anek']
)
async def say(ctx):
    if (ctx.author.voice):
        
        if save_anek(get_anek()) == 'success':
            channel = ctx.message.author.voice.channel
            voice = await channel.connect()
            source = FFmpegPCMAudio(
                executable="ffmpeg/ffmpeg.exe", source="audio/anek.mp3")
            player = voice.play(source)

            for x in bot.voice_clients:
                if (x.server == ctx.message.server):
                    return await x.disconnect()
