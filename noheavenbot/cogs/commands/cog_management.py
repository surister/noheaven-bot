from discord.ext.commands import command

from noheavenbot.utils.cogs_manager import load_cogs, unload_cogs


class CogManagement:

    def __init__(self, bot):
        self.bot = bot

    @command(pass_context=True)
    async def reload(self, ctx):

        unload_cogs(self.bot)
        await ctx.send('Cogs unloaded')
        load_cogs(self.bot)
        await ctx.send('Cogs reloaded')


def setup(bot):
    bot.add_cog(CogManagement(bot))
