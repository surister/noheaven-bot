import aiohttp
import io
import random

from bs4 import BeautifulSoup

from discord import File
from discord.ext import commands

from utils.constants import nsfw_categories


def is_nsfw(ctx):
    return ctx.channel.is_nsfw()


class Fun:

    def __init__(self, bot):
        self.bot = bot

    @commands.check(is_nsfw)
    @commands.group(invoke_without_command=True, aliases=['p'])
    @commands.cooldown(2, 5)
    async def porn(self, ctx, arg):

            if arg.lower() not in nsfw_categories:
                return await ctx.send('Wrong category')

            async with ctx.channel.typing():
                link = f'http://www.sex.com/pics/{arg.lower()}/'
                async with aiohttp.ClientSession() as session:
                    async with session.get(link) as resp:
                        full_html = await resp.text()
                soup = BeautifulSoup(full_html, 'html.parser')

                images = [link.get('data-src') for link in soup.find_all('img') if link.get('data-src')]  #
                # link.get('data-src') can also return None
                async with aiohttp.ClientSession() as session:
                    async with session.get(random.choice(images)) as resp:
                        if resp.status != 200:
                            return await ctx.channel.send('Could not download file...')
                        data = io.BytesIO(await resp.read())
                        await ctx.channel.send(file=File(data, 'cool_image.png'))

    @commands.check(is_nsfw)
    @commands.group(invoke_without_command=True, aliases=['g'])
    @commands.cooldown(2, 5)
    async def gif(self, ctx, arg):

            if arg.lower() not in nsfw_categories:
                return await ctx.send('Wrong category')

            async with ctx.channel.typing():
                link = f'http://www.sex.com/gifs/{arg.lower()}/'
                async with aiohttp.ClientSession() as session:
                    async with session.get(link) as resp:
                        full_html = await resp.text()
                soup = BeautifulSoup(full_html, 'html.parser')

                images = [link.get('data-src') for link in soup.find_all('img') if link.get('data-src')]

                await ctx.channel.send(random.choice(images))

    @staticmethod
    async def nsfw_list(ctx):
        await ctx.channel.send("** - **".join(nsfw_categories))

    @gif.command(name='list')
    async def _list(self, ctx):
        await Fun.nsfw_list(ctx)

    @porn.command(name='list')
    async def __list(self, ctx):
        await Fun.nsfw_list(ctx)


def setup(bot):
    bot.add_cog(Fun(bot))
