from discord.ext.commands import command, Cog


class Test(Cog):

    def __init__(self, bot):
        self.bot = bot

    @command()
    async def test(self, ctx):

        for name in ctx.guild.members:
            print(f"(Default,'{name.id}','{name.name}',{name.discriminator},{str(name.bot).lower()}),")


def setup(bot):
    bot.add_cog(Test(bot))
