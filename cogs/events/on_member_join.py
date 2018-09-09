from discord.utils import get


class OnMemberActions:

    def __init__(self, bot):
        self.bot = bot

    async def on_member_join(self, member):

        recepcion = self.bot.get_channel(452530575618867200)
        await recepcion.send(f'Bienvenido {member.mention} a {member.guild.name}')

        role = get(member.guild.roles, name='Friends')
        await member.add_roles(role)


def setup(bot):
    bot.add_cog(OnMemberActions(bot))
