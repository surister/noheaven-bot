from typing import Union, List

import asyncio
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

    @classmethod
    def create_playlist(cls, name: str) -> None:
        cls.number_of_playlists += 1
        playlist_name = name or cls.number_of_playlists
        Json.make_new_index(cls.FP, [], playlist_name=playlist_name)

    @classmethod
    def delete_playlist(cls, index: int) -> None:
        f = Json.get(cls.FP)
        f.pop(index)
        Json.make_new_index(cls.FP, f)


class Voice:
    def __init__(self, bot, ctx):
        """Class that controls the bot voice"""
        self.voice_client = ctx.voice_client  # ctx.voice_client
        self.bot = bot
        self.queue = asyncio.Queue()
        self.flow_control = asyncio.Event()
        self.audio_player = self.bot.loop.create_task(self.play_music())
        self.playing_music = True

    def _next(self):
        self.bot.loop.call_soon_threadsafe(self.flow_control.set)

    async def wait_until_ready(self):
        # Checks every 5 seconds if the song is finished, this is a workaround since after= doesn't work
        while True:
            if not self.voice_client.is_playing():
                break
            await asyncio.sleep(10)
        self._next()

    async def play_music(self):

        while self.playing_music:
            self.flow_control.clear()

            self.current_song = await self.queue.get()

            player = await YTDLSource.from_url(self.current_song, loop=self.bot.loop, stream=True)
            self.voice_client.play(source=player)  # Not using cus after kw doesn't work for some reason.

            await self.wait_until_ready()
            await self.flow_control.wait()


class Music:
    def __init__(self, bot):
        self.bot = bot
        self.temp_playlist = []
        self.random_play = False

        self.voice_states = {}


    """
    Bot is always going to be playing music from a playlist, whether it's a temporal one created by just concatenating
    !play <song> calls or one created by the user manually.
    """
    #   -------- <Utility functions>
    def get_voice_state(self, guild, ctx):

        state = self.voice_states.get(guild.id)
        if state is None:
            state = Voice(self.bot, ctx)
            self.voice_states[guild.id] = state

        return state

    @staticmethod
    async def get_current_channel(ctx) -> discord.VoiceChannel:
        for channel in ctx.guild.channels:
            if isinstance(channel, discord.channel.VoiceChannel):
                if ctx.author in channel.members:
                    return channel

    @property
    def playlist_index(self):
        return [index for index in Json.get(Playlist.FP)]

    @commands.command(name='continue')
    async def _continue(self, ctx):
        ctx.voice_client.resume()

    @commands.command()
    async def play(self, ctx, *, song=None):
        state = self.get_voice_state(ctx.guild, ctx)
        await state.queue.put(song)
        self.temp_playlist.append(song)

    @commands.command()
    async def pause(self, ctx):
        ctx.voice_client.pause()

    @commands.command()
    async def stop(self, ctx):
        await ctx.voice_client.disconnect()

    @commands.command()
    async def volume(self, ctx, volume: int = None):

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

    @play.before_invoke
    async def join(self, ctx) -> None:
        channel = await self.get_current_channel(ctx)
        if ctx.voice_client is not None:
            return await ctx.voice_client.move_to(channel)
        await channel.connect()

    @commands.group()
    async def playlist(self, ctx):
        ...
    # TODO
    # Delete playlist command
    # Delete song from <playlist> command
    # Make playlist from temporal playlist
    # Play a playlist command (!playlist test1 play)
    # Play a playlist randomly command (!play test1 play random)

    @playlist.command()
    async def make(self, ctx, *, name=None):
        if name in self.playlist_index:
            return await ctx.send('This playlist already exists')
        Playlist.create_playlist(name)
        return await ctx.send(f'Se ha creado la playlist {name}')

    @playlist.command()
    async def add(self, ctx, name, *, url):
        if name not in self.playlist_index:
            return await ctx.send('Esa playlist no existe')
        Json.add_new_value(Playlist.FP, name, url)
        return await ctx.send(f'Se ha añadido la canción **{url}** a la playlist **{name}**')


def setup(bot):
    bot.add_cog(Music(bot))
