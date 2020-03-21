from discord.ext.commands import command, Cog
from noheavenbot.utils.constants import TEXTCHANNELS
from discord import Member


class Test(Cog):

    def __init__(self, bot):
        self.bot = bot

    @command()
    async def test(self, ctx, bot: Member):
        print(str(ctx.message.author.id), ctx.message.author.nick, str(bot.id), bot.display_name)


def setup(bot):
    bot.add_cog(Test(bot))
