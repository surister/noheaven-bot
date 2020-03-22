from discord.ext.commands import Cog, command, has_role

from noheavenbot.utils.database_tables.table_users import Users


class DatabaseCommands(Cog):
    """Commands to direclty interact with the db, shouldn't be really used."""

    def __init__(self, bot):
        self.bot = bot

    @has_role('Server Admin')
    @command(name='syncdb')
    async def sync_db(self, ctx):

        values = []
        guild_members_len: int = len(ctx.message.guild.members)
        db_members_len: int = await Users.len()

        if guild_members_len > db_members_len:
            await ctx.send(f'Faltan {guild_members_len - db_members_len} por sincronizar')
            db_user_list = await Users.get_users_identifiers_list()
            for d_user in ctx.message.guild.members:
                if not db_user_list.__contains__(str(d_user.id)):
                    values.append((d_user.name, d_user.bot, int(d_user.discriminator), str(d_user.id)))

            await Users.insert_many(values)

        await ctx.send('Sincronizados')


def setup(bot):
    bot.add_cog(DatabaseCommands(bot))
