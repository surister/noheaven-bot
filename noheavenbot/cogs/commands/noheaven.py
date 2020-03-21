"""
Group of commands that only no heaven members have access to.
"""

from discord import Member
from discord.ext.commands import Cog, command, has_role
from noheavenbot.utils.database_tables import TrustedBot
from noheavenbot.utils.validator import has_role as check_role


class NhCommands(Cog):

    def __init__(self, bot):
        self.bot = bot

    @has_role('NoHeaven')
    @command(name='addbot')
    async def add_bot(self, ctx, bot: Member, is_admin: bool = False):
        admin = is_admin

        if is_admin:
            if check_role(ctx.message.author.roles, 455390225657757706, True):
                admin = True
            else:
                return await ctx.send('Solo los administradores pueden añadir bots con permisos de administración.')

        await TrustedBot.insert_bot(str(ctx.message.author.id), ctx.message.author.nick, str(bot.id), bot.display_name, admin)

        if admin:
            # admin bot 455390225657757706
            # normal bot 688044129489649738

            role = ctx.guild.get_role(455390225657757706)
        else:
            role = ctx.guild.get_role(688044129489649738)

        await bot.add_roles(role)
        return await ctx.send(f'Añadido el rango de bot a {bot.mention}!')


def setup(bot):
    bot.add_cog(NhCommands(bot))
