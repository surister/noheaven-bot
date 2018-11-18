import asyncio

from collections import deque

import discord
import youtube_dl

from discord.ext import commands

from noheavenbot.utils.constants import Path
from noheavenbot.utils.json_utils import Json

# Suppress noise about console usage from errors
youtube_dl.utils.bug_reports_message = lambda: ''

ytdl_format_options = {
    'format': 'bestaudio/best',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0' # bind to ipv4 since ipv6 addresses cause issues sometimes
}

ffmpeg_options = {
    'options': '-vn'
}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)


class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.3):
        super().__init__(source, volume)

        self.data = data

        self.title = data.get('title')
        self.url = data.get('url')

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))

        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]

        filename = data['url'] if stream else ytdl.prepare_filename(data)
        return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data)


class Playlist:
    FP = f'{Path.COMMANDS}/playlist.json'
    number_of_playlists = len(Json.get(FP))

    current_playlist = None

    temp_playlist = ()

    @classmethod
    def create_playlist(cls, name: str) -> None:
        cls.number_of_playlists += 1
        playlist_name = name or cls.number_of_playlists
        Json.write(cls.FP, [], playlist_name=playlist_name)

    @classmethod
    def delete_playlist(cls, index: int) -> None:
        f = Json.get(cls.FP)
        f.pop(index)
        Json.write(cls.FP, f)


class Music:
    def __init__(self, bot):
        self.bot = bot
        self.current_playlist = None

    @staticmethod
    async def get_current_channel(ctx):
        for channel in ctx.guild.channels:
            if isinstance(channel, discord.channel.VoiceChannel):
                if ctx.author in channel.members:
                    return channel

    @commands.command()
    async def join(self, ctx):
        """Joins a voice channel"""
        channel = await self.get_current_channel(ctx)
        if ctx.voice_client is not None:
            return await ctx.voice_client.move_to(channel)

        await channel.connect()

    @commands.group()
    async def playlist(self, ctx):
        pass

    @playlist.command()
    async def make(self, ctx, *, name=None):
        Playlist.create_playlist(name)

    @commands.command()
    async def play(self, ctx, *, url):
        """Streams from a url (same as yt, but doesn't predownload)"""

        async with ctx.typing():
            player = await YTDLSource.from_url(url, loop=self.bot.loop, stream=True)
            ctx.voice_client.play(player, after=lambda e: print('Player error: %s' % e) if e else None)

        await ctx.send('Now playing: {}'.format(player.title))

    @commands.command()
    async def pause(self, ctx):
        ctx.voice_client.pause()

    @commands.command()
    async def resume(self, ctx):
        ctx.voice_client.resume()

    @commands.command()
    async def volume(self, ctx, volume: int = None):
        """Changes the player's volume"""

        if not hasattr(ctx.voice_client.source, 'volume'):
            return await ctx.send('El volumen actual es 100%')

        if ctx.voice_client is None:
            return await ctx.send("Not connected to a voice channel.")

        if volume is None:
            return await ctx.send(f'El volumen actual es {int((ctx.voice_client.source.volume * 100) / 0.5)}%')

        if 0 > volume < 100:
            return await ctx.send('Volumen tiene que ser entre 0 y 100')

        ctx.voice_client.source.volume = (volume * 0.5) / 100

        await ctx.send(f'El volumen esta ahora al {volume}%')

    @commands.command()
    async def stop(self, ctx):
        """Stops and disconnects the bot from voice"""
        await ctx.voice_client.disconnect()

    @play.before_invoke
    async def ensure_voice(self, ctx):
        if ctx.voice_client is None:
            if ctx.author.voice:
                await ctx.author.voice.channel.connect()
            else:
                await ctx.send("You are not connected to a voice channel.")
                raise commands.CommandError("Author not connected to a voice channel.")
        elif ctx.voice_client.is_playing():
            ctx.voice_client.stop()


def setup(bot):
    bot.add_cog(Music(bot))
