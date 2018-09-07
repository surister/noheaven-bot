import random
import time

import io
import aiohttp

from bs4 import BeautifulSoup

from discord import File
from discord.ext import commands
from discord import Embed


def is_sur(ctx):
    return ctx.channel.id == 452526547635535893


class Fun:

    def __init__(self, bot):
        self.bot = bot

    @commands.check(is_sur)
    @commands.command()
    async def hentai(self, ctx):

        async with aiohttp.ClientSession() as session:
            async with session.get('http://www.sex.com/pics/hentai/') as resp:
                full_html = await resp.text()
        soup = BeautifulSoup(full_html, 'html.parser')

        images = [link.get('data-src') for link in soup.find_all('img') if link.get('data-src')]

        async with aiohttp.ClientSession() as session:
            async with session.get(random.choice(images)) as resp:
                if resp.status != 200:
                    return await ctx.channel.send('Could not download file...')
                data = io.BytesIO(await resp.read())
                await ctx.channel.send(file=File(data, 'cool_image.png'))

    @commands.check(is_sur)
    @commands.command()
    async def porn(self, ctx, arg):
        if arg == 'list':
            embed = Embed(title='Lista de categorias')

            cat =['Amateur Anal Asian Ass Babes BBW BDSM Big Tits Blonde Blowjob Brunette Celebrity College Creampie Cumshots'
             ' Double Penetration Ebony Emo female-ejaculation Fisting footjob Gangbang Gay Girlfriend Group Sex Hairy'
             ' Handjob Hardcore Hentai Indian Interracial Latina Lesbian Lingerie Masturbation Mature MILF Non-Nude '
             'Panties penis Pornstar Public Sex Pussy Redhead Self Shot Shemale Teen (18+) Threesome Toys']
            embed.add_field(name='Disfrutad.', value=cat[0])
            await ctx.channel.send(embed=embed)
        else:

            link = f'http://www.sex.com/pics/{arg.lower()}/'
            async with aiohttp.ClientSession() as session:
                async with session.get(link) as resp:
                    full_html = await resp.text()
            soup = BeautifulSoup(full_html, 'html.parser')

            images = [link.get('data-src') for link in soup.find_all('img') if link.get('data-src')]

            async with aiohttp.ClientSession() as session:
                async with session.get(random.choice(images)) as resp:
                    if resp.status != 200:
                        return await ctx.channel.send('Could not download file...')
                    data = io.BytesIO(await resp.read())
                    await ctx.channel.send(file=File(data, 'cool_image.png'))

    @commands.check(is_sur)
    @commands.command()
    async def gif(self, ctx, arg):
        if arg == 'list':
            embed = Embed(title='Lista de categorias')

            cat =['Amateur Anal Asian Ass Babes BBW BDSM Big Tits Blonde Blowjob Brunette Celebrity College Creampie Cumshots'
             ' Double Penetration Ebony Emo female-ejaculation Fisting footjob Gangbang Gay Girlfriend Group Sex Hairy'
             ' Handjob Hardcore Hentai Indian Interracial Latina Lesbian Lingerie Masturbation Mature MILF Non-Nude '
             'Panties penis Pornstar Public Sex Pussy Redhead Self Shot Shemale Teen (18+) Threesome Toys']
            embed.add_field(name='Disfrutad.', value=cat[0])
            await ctx.channel.send(embed=embed)
        else:

            link = f'http://www.sex.com/gifs/{arg.lower()}/'
            async with aiohttp.ClientSession() as session:
                async with session.get(link) as resp:
                    full_html = await resp.text()
            soup = BeautifulSoup(full_html, 'html.parser')

            images = [link.get('data-src') for link in soup.find_all('img') if link.get('data-src')]

            await ctx.channel.send(random.choice(images))


def setup(bot):
    bot.add_cog(Fun(bot))
