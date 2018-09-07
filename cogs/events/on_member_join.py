

class Onmember_actions:

    def __init__(self, bot):
        self.bot = bot

    async def on_member_join(self, member):
        recepcion = self.bot.get_channel(452530575618867200)
        await recepcion.send(f'Bienvenido {member.name} a {member.guild.name}')


def setup(bot):
    bot.add_cog(Onmember_actions(bot))