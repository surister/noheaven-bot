from noheavenbot.utils import DatabaseConnection, GarchTable
from discord.ext.commands import command, group


class DatabaseInfoInjector:
    def __init__(self, bot):
        self.bot = bot

    @group(invoke_without_command=True)
    async def garch(self, ctx):
        await ctx.send(await GarchTable.fetch_name())

    @garch.command()
    async def save(self, ctx, *, name):
        await GarchTable.insert_row(name)
        await ctx.send(f'Gardado: {name}')

    @garch.command(name='del')
    async def _del(self, ctx, index):
        try:
            index = int(index)
        except ValueError:
            return await ctx.send('')

        if index <= await GarchTable.get_max_index():
            return await ctx.send('Ese index no existe')
        await GarchTable.remove_row(index)

    @garch.command()
    async def list(self, ctx):

        name_list = await GarchTable.fetch_all()
        name_list.insert(0, '\u200b')
        await ctx.send('\n'.join(name_list))


def setup(bot):
    bot.add_cog(DatabaseInfoInjector(bot))
