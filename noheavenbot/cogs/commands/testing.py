from discord.ext.commands import command, Cog
from noheavenbot.utils.constants import TEXTCHANNELS

class Test(Cog):

    def __init__(self, bot):
        self.bot = bot

    @command()
    async def test(self, ctx):
        await ctx.send(TEXTCHANNELS.__getattribute__('bot-commands'))


def setup(bot):
    bot.add_cog(Test(bot))
