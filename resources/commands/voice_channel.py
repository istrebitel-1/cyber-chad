from youtube_dl import YoutubeDL
from discord.player import FFmpegPCMAudio

from resources import bot
from resources.voice import save_anek, get_anek


class Queue:
    """Очередь трецков"""
    def __init__(self) -> None:
        self.tracks_url = []

    def append_track(self, url):
        """Добавление трека в куеуе"""
        self.tracks_url.append(url)

    def pop_track(self):
        """попит левый трецк"""
        self.tracks_url.pop(0)

    def clear_queue(self):
        """Очищает очередб"""
        self.tracks_url = []


tracks_queue = Queue()


@bot.command(
    name='podliva_join',
    aliases=['join', 'get_your_ass_back_here'],
)
async def join(ctx):
    """Join voice channel and says 'nice c**k''"""
    if (ctx.author.voice):
        channel = ctx.message.author.voice.channel
        voice = await channel.connect()
        source = FFmpegPCMAudio(
            executable="ffmpeg/ffmpeg.exe",
            source="audio/nc.mp3",
        )
        voice.play(source)


@bot.command(
    name='podliva_leave',
    aliases=['leave', 'fuck_you'],
)
async def leave(ctx):
    """Leave voice channel"""
    if (ctx.voice_client):
        await ctx.guild.voice_client.disconnect()
    else:
        pass


@bot.command(
    name='say',
    aliases=['anek'],
)
async def say(ctx):
    """Say anek from mp3 file"""
    if (ctx.author.voice):

        if save_anek(get_anek()) == 'success':
            channel = ctx.message.author.voice.channel
            voice = await channel.connect()
            source = FFmpegPCMAudio(
                executable="ffmpeg/ffmpeg.exe",
                source="audio/anek.mp3",
            )
            voice.play(source)

            await ctx.guild.voice_client.disconnect()


@bot.command(
    name='play',
    aliases=['p'],
)
async def play(ctx, youtube_url):
    """Plays youtube audio"""
    YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist': 'False'}
    FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
    if (ctx.author.voice):
        channel = ctx.message.author.voice.channel

        try:
            voice = await channel.connect()
        except Exception:
            voice = channel

        tracks_queue.clear_queue()
        tracks_queue.append_track(youtube_url)

        for url in tracks_queue.tracks_url:
            with YoutubeDL(YDL_OPTIONS) as ydl:
                info = ydl.extract_info(url, download=False)
            URL = info['formats'][0]['url']
            voice.play(FFmpegPCMAudio(URL, **FFMPEG_OPTIONS))
            voice.is_playing()
            tracks_queue.pop_track()

    else:
        await ctx.send("Already playing song")
        return


@bot.command(
    name='queye',
    aliases=['куеуе', 'q']
)
async def queue(ctx, url):
    """Add track to queue"""
    tracks_queue.append_track(url)
    await ctx.send("Добавлен трецк флек$$овый")


@bot.command(
    name='clear',
)
async def clear(ctx):
    """Clear tracks queue"""
    tracks_queue.clear_queue()
    await ctx.send("Очередь очищена")
