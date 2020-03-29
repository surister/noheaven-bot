from discord.ext.commands import command, Cog
from noheavenbot.utils.constants import TEXTCHANNELS
from discord import Member
from noheavenbot.utils.database_tables.table_users import Users
from noheavenbot.utils.validator import has_role as check_role


class Test(Cog):

    def __init__(self, bot):
        self.bot = bot

    @command()
    async def test(self, ctx):
        if check_role(ctx.message.author.roles, 445947005169303552, True):
            admin = True
            return await ctx.send('all ok')
        else:
            return await ctx.send('Solo los administradores pueden añadir bots con permisos de administración.')


def setup(bot):
    bot.add_cog(Test(bot))
