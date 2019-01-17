import random
from typing import Union

import asyncio
import discord
import youtube_dl
from discord.ext.commands import command, group, has_role

from noheavenbot.utils.constructors import EmbedConstructor
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
    'source_address': '0.0.0.0'  # bind to ipv4 since ipv6 addresses cause issues sometimes
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
    NUMBER_OF_PLAYLISTS = len(Json.get(FP))

    @classmethod
    def create_playlist(cls, name: str=None) -> None:
        cls.NUMBER_OF_PLAYLISTS += 1
        playlist_name = name or cls.NUMBER_OF_PLAYLISTS
        Json.make_new_index(cls.FP, [], playlist_name=playlist_name)

    @classmethod
    def delete_playlist(cls, index: Union[int, str]) -> None:
        f = Json.get(cls.FP)
        f.pop(index)
        Json.rewrite(cls.FP, f)

    @classmethod
    def get_elements_from_index(cls, index: Union[int, str]):
        f = Json.get(cls.FP)
        return f[index]

    @classmethod
    def add_element_to_index(cls, name, url: Union[str, list]):
        if isinstance(url, list):
            for _url in url:
                Json.add_new_value(Playlist.FP, name, _url)
        else:
            Json.add_new_value(Playlist.FP, name, url)

    @classmethod
    def delete_element_from_playlist(cls, index, url):
        Json.delete_value(Playlist.FP, index, url)

    @classmethod
    def playlist_index(cls):
        return [index for index in Json.get(cls.FP)]


class Voice:
    def __init__(self, bot, ctx):
        """Class that controls the bot voice"""
        self.ctx = ctx
        self.voice_client = ctx.voice_client
        self.bot = bot
        self.queue = asyncio.Queue()
        self.flow_control = asyncio.Event()
        self.audio_player = self.bot.loop.create_task(self.play_music())
        self.playing_music = True
        self.play_playlist = False
        self.random_playlist = False
        self.playlist = None

    def update_voice_client_connection(self, client: discord.VoiceClient) -> None:
        self.voice_client = client

    def update_ctx(self, ctx) -> None:
        self.ctx = ctx

    def activate_playlist(self, index, _random=None) -> None:
        self.play_playlist = True
        self.playlist_index = index
        self.playlist = Playlist.get_elements_from_index(index)
        if _random:
            self.random_playlist = True

    def deactivate_playlist(self) -> None:
        self.playlist = None
        self.play_playlist = False
        self.random_playlist = False

    @property
    def get_ctx(self):
        return self.ctx

    @property
    def get_client(self) -> discord.VoiceClient:
        return self.voice_client

    async def notify_song(self, player):
        embed = discord.Embed(title=f'Tocando ahora: **{player.title}**')
        embed.add_field(name=f'Canción pedida por {self.ctx.author}', value=player.data['webpage_url'])
        if self.play_playlist:
            embed.add_field(name=f'Playlist: {self.playlist_index}',
                            value=f'modo {"random" if self.random_playlist else "normal"}', inline=False)
        await self.ctx.send(embed=embed)

    async def notify_queue(self, song):
        embed = discord.Embed(title=f'La canción **{song}** se ha añadido a la cola')
        embed.add_field(name=f'Canción pedida por {self.ctx.author}', value='\u200b')
        await self.ctx.send(embed=embed)

    def _next(self) -> None:
        self.bot.loop.call_soon_threadsafe(self.flow_control.set)

    async def check_if_finished(self):
        # Checks every 5 seconds if the song is finished, this is a workaround since after= doesn't work
        timeout = 0

        while True:
            if not self.voice_client.is_playing() and self.queue.qsize() != 0 or\
                    not self.voice_client.is_playing() and self.play_playlist:
                break

            if timeout > 60 and not self.voice_client.is_playing() and self.voice_client.is_connected():
                await self.ctx.send('Llevo un minuto sin poner musica, me voy a desconectar que me aburro.')
                await self.voice_client.disconnect()

                break
            await asyncio.sleep(5)

            if not self.voice_client.is_playing():
                timeout += 5
        self._next()

    async def play_music(self):
        current_song = ''
        playlist_index = 0
        while True:
            self.flow_control.clear()
            # Once the task is created, it will always run, once teh queu runs out of songs to play or the bot disc.
            # it will wait to get a new queue entry to play again. It is sure that it will be play since commands
            # like !play have to be used to add a new entry, and that command makes all the necessary checks/updates
            # to make everything work
            if not self.play_playlist:
                current_song = await self.queue.get()
            else:
                try:
                    if self.random_playlist:
                        current_song = random.choice(self.playlist)
                    else:
                        current_song = self.playlist[playlist_index]
                        playlist_index += 1
                except IndexError:
                    self.deactivate_playlist()
            player = await YTDLSource.from_url(current_song, loop=self.bot.loop, stream=True)
            await self.notify_song(player)
            self.voice_client.play(source=player)  # Not using cus after kw doesn't work for some reason.
            await self.check_if_finished()
            await self.flow_control.wait()


class Music:
    def __init__(self, bot):
        self.bot = bot
        self.temp_playlist = []
        self.random_play = False

        self.voice_states = {}
        self.voice_client = None
        # The bot voice client, got from bot.connect() and updated every time the bot joins a channel

    """
    Bot is always going to be playing music from a playlist, whether it's a temporal one created by just concatenating
    !play <song> calls or one created by the user manually.
    """
    #   -------- <Utility functions>
    def update_basic_ctx_or_voice(self, ctx, state) -> None:
        """
        Checks whether client_voice or ctx objects need to be updated, if so, updates them.
        """
        if self.voice_client is not state.get_client:  # 1
            state.update_voice_client_connection(ctx.voice_client)
        if ctx is not state.get_ctx:
            state.update_ctx(ctx)

    def get_voice_state(self, ctx):
        guild = ctx.guild
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

    # -------- </...>

    @command(name='continue')
    async def _continue(self, ctx):
        ctx.voice_client.resume()

    @command()
    async def play(self, ctx, *, song=None):
        """
        # 1
        We check whether the current voice_client is still relevant. Why? Because when the bot leaves a channel
        the voice_client attr in Voice is still alive and will be until the code disconnects, but that voice_connection
        is not functional anymore since once the bot rejoins the channel, a new voice connection will be created,
        so we check if the one the Voice class is going to use and the current voice_client is the same, if it is not
        we just update it. This ensures total continuity among channel connections in different servers.
        """
        state = self.get_voice_state(ctx)
        self.update_basic_ctx_or_voice(ctx, state)
        if song is not None:
            if ctx.voice_client.is_playing():
                await state.notify_queue(song)
            await state.queue.put(song)
            self.temp_playlist.append(song)
        else:
            await ctx.send('¿¡Pero que quieres que toque!?')

    @command()
    async def skip(self, ctx):
        self.voice_client.stop()
        await ctx.send('Pasando de esta canción!')

    @command()
    async def pause(self, ctx):
        ctx.voice_client.pause()
        await ctx.send('Música pausada!')

    @command()
    async def stop(self, ctx):
        await ctx.voice_client.disconnect()
        await ctx.send('Hasta luego!')

    @command()
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
    async def join(self, ctx) -> Union[None, discord.VoiceClient]:
        channel = await self.get_current_channel(ctx)
        if ctx.voice_client is not None:
            return await ctx.voice_client.move_to(channel)
        if channel is not None:
            self.voice_client = await channel.connect()  # Updates voice_client when joining the channel
            return
        return await ctx.send('No estás conectado a un canal de voz')

    @group(invoke_without_command=True)
    async def temp(self, ctx):
        l = self.temp_playlist
        if not self.temp_playlist:
            return await ctx.send('La playlist temporal esta vacia')
        await ctx.send(" - ".join(map(lambda x, y: f'{x[0]}: **{y}**', (enumerate(l)), l)))

    @temp.command(name='d')
    async def temp_delete(self, ctx, index: int):
        if not isinstance(index, int):
            return await ctx.send('El índice tiene que ser un número')
        deleted_song = self.temp_playlist[index]
        self.temp_playlist.pop(index)
        await ctx.send(f'Borrado la canción {deleted_song}')
        await self.bot.get_command('temp').invoke(ctx)

    @temp.command()
    async def copy(self, ctx, name: str):
        if not name:
            return await ctx.send('Por favor ponle un nombre')
        Playlist.create_playlist(name)
        Playlist.add_element_to_index(name, self.temp_playlist)
        await ctx.send(f'Creada la playlist {name}')

    @group(invoke_without_command=True)
    async def playlist(self, ctx):
        """
        Shows playlist information:

            #5
        """
        a = [(f'{index} - Total canciones {len(Playlist.get_elements_from_index(index))}',
              " - ".join(Playlist.get_elements_from_index(index)[:3]) or 'Vacio') for index in Playlist.playlist_index()[:5]]
        info_embed = EmbedConstructor('Playlists', a).construct()
        await ctx.send(embed=info_embed)

    @playlist.command(name="p")
    async def _play(self, ctx, index: str, _random: str= None):
        await self.join(ctx)
        state = self.get_voice_state(ctx)
        if self.voice_client is not state.get_client:
            state.update_voice_client_connection(ctx.voice_client)
        state.activate_playlist(index, _random)
        state._next()

    # TODO
    # 5 Use paginator to improve playlists info?

    @playlist.command()
    async def make(self, ctx, *, name: str = None):
        if name in Playlist.playlist_index():
            return await ctx.send('This playlist already exists')
        Playlist.create_playlist(name)
        return await ctx.send(f'Se ha creado la playlist {name}')

    @playlist.command()
    async def add(self, ctx, index, *, url):
        if index not in Playlist.playlist_index():
            return await ctx.send('Esa playlist no existe')
        Playlist.add_element_to_index(index, url)
        return await ctx.send(f'Se ha añadido la canción **{url}** a la playlist **{index}**')

    @has_role('NoHeaven')
    @playlist.command(name='dels')
    async def __del(self, ctx, index, *, url):
        try:
            Playlist.delete_element_from_playlist(index, url)
        except ValueError:
            return await ctx.send('Esta canción no esta en la playlist')

    @has_role('NoHeaven')
    @playlist.command(name='del')
    async def _del(self, ctx, *, index):
        if index not in Playlist.playlist_index():
            return await ctx.send('Esa playlist no existe')
        Playlist.delete_playlist(index)
        await ctx.send(f'Se ha borrado la playlist {index}')


def setup(bot):
    bot.add_cog(Music(bot))
