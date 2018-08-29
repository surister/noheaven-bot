from discord.ext import commands
from utils.cogs_manager import load_cogs, unload_cogs


class Cog_Management:

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def reload(self, ctx):

        unload_cogs(self)
        ctx.send('Cogs unloaded')
        load_cogs(self)
        ctx.send('Cogs reloaded')


def setup(bot):
    bot.add_cog(Cog_Management(bot))
