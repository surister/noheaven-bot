from noheavenbot.utils.database_tables import table_garch
from discord.ext.commands import group, Cog


class DatabaseInfoInjector(Cog):
    def __init__(self, bot):
        self.bot = bot

    @group(invoke_without_command=True)
    async def garch(self, ctx):
        await ctx.send(f'{await table_garch.Garch.fetch_name()}')

    @garch.command(aliases=['add'])
    async def save(self, ctx, *, name):
        await table_garch.Garch.insert_row(name)
        await ctx.send(f'Gardado: {name}')

    @garch.command(name='del')
    async def remove(self, ctx, index):
        try:
            index = int(index)
        except ValueError:
            return await ctx.send('El índice tiene que ser un número.')

        if index < await table_garch.Garch.get_max_index():
            return await ctx.send('Ese índice no existe')
        await table_garch.Garch.remove_row(index)
        await ctx.send(f'He borrado el nombre de índice {index}')

    @garch.command()
    async def list(self, ctx):

        name_list = await table_garch.Garch.fetch_all()
        name_list.insert(0, '\u200b')
        await ctx.send('\n'.join(name_list))


def setup(bot):
    bot.add_cog(DatabaseInfoInjector(bot))
