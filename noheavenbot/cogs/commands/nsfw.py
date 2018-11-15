import aiohttp
import io
import random

from typing import List

from bs4 import BeautifulSoup

from discord import File
from discord.ext import commands

from noheavenbot.utils.constants import nsfw_categories, nsfw_lol


def filter_crap(l: List[str])-> List[str]:
    craps = ['i', '.', 'i', '/', '#', 'h', 'pass', 'http', 'index',
             'https', 'comments', 'register', '#inline', 'password']
    _set = set(l)
    temp_set = _set.copy()
    for i in _set:
        for crap in craps:
            if i.startswith(crap):
                temp_set.remove(i)
                break
    temp_list = list(temp_set)
    return temp_list


def is_nsfw(ctx):
    return ctx.channel.is_nsfw()


class Fun:

    def __init__(self, bot):
        self.bot = bot

    @commands.check(is_nsfw)
    @commands.group(invoke_without_command=True, aliases=['p'])
    @commands.cooldown(2, 5)
    async def porn(self, ctx, arg):
            src = 'data-src'
            link = f'http://www.sex.com/pics/{arg.lower()}/'

            if arg.lower() not in nsfw_categories:
                return await ctx.send('Wrong category')

            if arg.lower() not in nsfw_lol and ctx.invoked_with == 'lol':
                return await ctx.send('Wrong category')

            async with ctx.channel.typing():
                async with aiohttp.ClientSession() as session:
                    async with session.get(link) as resp:
                        full_html = await resp.text()
                soup = BeautifulSoup(full_html, 'html.parser')

                images = [link.get(src) for link in soup.find_all('img') if link.get(src)]  #

                # link.get('data-src') can also return None
                async with aiohttp.ClientSession() as session:
                    async with session.get(random.choice(images)) as resp:
                        if resp.status != 200:
                            return await ctx.channel.send('Could not download file...')
                        data = io.BytesIO(await resp.read())
                        await ctx.channel.send(file=File(data, 'cool_image.png'))


    # lol command is very similar to porn one, only changes the way the html is being parsed, the good way would be
    # to make it work regardless of the webpage html organization (kinda difficult) but i'm lazy, feel free to mr/pr
    @commands.check(is_nsfw)
    @commands.group(invoke_without_command=True, aliases=['lol'])
    @commands.cooldown(2, 5)
    async def _lol(self, ctx, arg):
        src = 'href'
        link = f'http://www.lolhentai.net/index?/category/{arg.lower()}/'

        if arg.lower() not in nsfw_lol:
            return await ctx.send('Wrong category')

        async with ctx.channel.typing():
            async with aiohttp.ClientSession() as session:
                async with session.get(link) as resp:
                    full_html = await resp.text()
            soup = BeautifulSoup(full_html, 'html.parser')

            images = [link.get(src) for link in soup.find_all('a') if link.get(src)]  #
            images = filter_crap(images)

            # link.get('data-src') can also return None
            img_link = f'http://www.lolhentai.net/{random.choice(images)}'
            print(img_link)
            async with ctx.channel.typing():
                async with aiohttp.ClientSession() as session:
                    async with session.get(link) as resp:
                        full_html = await resp.text()
                soup = BeautifulSoup(full_html, 'html5lib')
                print(soup)
                async with aiohttp.ClientSession() as session:
                    async with session.get(img_link) as resp:
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

# http://www.lolhentai.net/picture?/40855-2651186_ahri_league_of_legends_tofuubear/category
# http://www.lolhentai.net/_data/i/upload/2018/10/25/20181025185210-26dc9d44-me.jpg
