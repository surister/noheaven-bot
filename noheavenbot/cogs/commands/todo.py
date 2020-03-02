
from discord.ext.commands import command, check, has_role, Cog, group
from noheavenbot.utils.database_tables import Todo as todo_table


# TOdo logs aqui en todo


def is_allowed(ctx):
    return ctx.author.id == 462723469407158286
    # sur


class Todo(Cog):

    def __init__(self, bot):
        self.bot = bot

    @group()
    @check(is_allowed)
    async def todo(self, ctx):
        name_list = await todo_table.fetch_all()
        name_list.insert(0, '\u200b')
        await ctx.send('\n'.join(name_list))

    @todo.command()
    async def add(self, ctx, *, txt):
        await todo_table.insert_row(txt)
        ctx.send(f'Añadido, es el todo número {await todo_table.get_max_index() + 1}')

    @todo.command(aliases=['rem', 'del'])
    async def remove(self, ctx, n: int):
        try:
            index = int(n)
        except ValueError:
            return await ctx.send('El índice tiene que ser un número.')

        if index < await todo_table.get_max_index():
            return await ctx.send('Ese índice no existe')
        await todo_table.remove_row(n)
        await ctx.send(f'Borrado el todo número {n}')


def setup(bot):
    bot.add_cog(Todo(bot))
