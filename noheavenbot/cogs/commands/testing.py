from discord.ext.commands import command, Cog
from noheavenbot.utils.constants import TEXTCHANNELS
from discord import Member
from noheavenbot.utils.database_tables.table_users import Users


class Test(Cog):

    def __init__(self, bot):
        self.bot = bot

    @command()
    async def test(self, ctx):
        values = []
        if len(ctx.message.guild.members) > await Users.len():
            db_user_list = await Users.get_users_identifiers_list()
            for d_user in ctx.message.guild.members:
                if not db_user_list.__contains__(str(d_user.id)):
                    values.append((d_user.name, d_user.bot, int(d_user.discriminator), str(d_user.id)))

            await Users.insert_many(values)


def setup(bot):
    bot.add_cog(Test(bot))
