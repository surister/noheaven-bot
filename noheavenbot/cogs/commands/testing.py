from discord.ext.commands import command, Cog
from noheavenbot.utils.constants import TEXTCHANNELS
from discord import Member


class Test(Cog):

    def __init__(self, bot):
        self.bot = bot

    @command()
    async def test(self, ctx):
        pass


def setup(bot):
    bot.add_cog(Test(bot))
