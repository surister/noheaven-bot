import json
import random

from discord.ext import commands
from utils.path import utils_path


class Garch:

    def __init__(self, bot):
        self.bot = bot

    @commands.group(invoke_without_command=True)
    async def garch(self, ctx):
        with open(f'{utils_path}/garch.json', 'r') as gr:
            x = json.load(gr)
        await ctx.channel.send(random.choice(x['name']))

    @garch.command()
    async def save(self, ctx, *, arg):
        with open(f'{utils_path}/garch.json', 'r') as gr:
            x = json.load(gr)

        x['name'].append(arg)

        with open(f'{utils_path}/garch.json', 'w') as rg:
            json.dump(x, rg, indent=1)

    @garch.command()
    async def list(self, ctx):
        with open(f'{utils_path}/garch.json', 'r') as gr:
            x = json.load(gr)
        await ctx.send(x['name'])

    @garch.command(name='delete')
    async def _delete(self, ctx, index: int):
        with open(f'{utils_path}/garch.json', 'r') as gr:
            x = json.load(gr)

        fmt = x['name'][index]

        del x['name'][index]

        with open(f'{utils_path}/garch.json', 'w') as rg:
            json.dump(x, rg, indent=1)

        await ctx.send(f'Borrado {fmt}')


class Text:

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def text(self, ctx, *, message):
        b = message.lower().replace("$text", "")
        a = b.split()
        for i in a:
            c = ""
            for k in i:
                c = c + ":regional_indicator_{}:".format(k)
            await ctx.send(c)
        await ctx.channel.delete_messages([ctx.message])


def setup(bot):
    bot.add_cog(Garch(bot))
    bot.add_cog(Text(bot))