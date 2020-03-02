
from discord.ext.commands import command, check, has_role, Cog, group
from noheavenbot.utils.database_tables import Todo as todo_table


# TOdo logs aqui en todo


def is_allowed(ctx):
    return ctx.author.id == 462723469407158286
    # sur


class Todo(Cog):

    def __init__(self, bot):
        self.bot = bot

    @group(invoke_without_command=True)
    @check(is_allowed)
    async def todo(self, ctx):
        # if not await todo_table.get_max_index():
        name_list = await todo_table.fetch_all()
        name_list.insert(0, '\u200b')
        return await ctx.send('\n'.join(name_list))
        # return await ctx.send("No hay nada!")

    @todo.command()
    async def add(self, ctx, *, txt):
        await todo_table.insert_row(txt)
        await ctx.send(f'Añadido, es el todo número {await todo_table.get_max_index()}')

    @todo.command(aliases=['rem', 'del'])
    async def remove(self, ctx, n: int):
        try:
            index = int(n)
        except ValueError:
            return await ctx.send('El índice tiene que ser un número.')

        max_index = await todo_table.get_max_index()

        if not max_index:
            return await ctx.send('No hay nada!')
        if index > max_index:
            return await ctx.send('Ese índice no existe')

        await todo_table.remove_row(n)
        await ctx.send(f'Borrado el todo número {n}')

    @todo.command()
    async def test(self, ctx):
        return await ctx.send(await todo_table.get_max_index())


def setup(bot):
    bot.add_cog(Todo(bot))
