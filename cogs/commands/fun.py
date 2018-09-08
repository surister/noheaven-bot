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


def setup(bot):
    bot.add_cog(Garch(bot))
