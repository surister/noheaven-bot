import asyncio

import asyncpg

from discord.ext.commands import command


class DatabaseInfoInjector:
    def __init__(self, bot):
        self.bot = bot



    @command(name='use')
    async def get_users(self, ctx):
        db = await asyncpg.create_pool(**self.credentials)
        for member in ctx.guild.members:
            await db.execute('''
            INSERT INTO users (id, name, date, admin) VALUES ($1, $2, $3, $4)
            ''', member.id, member.display_name, member.joined_at, False)
        await db.close()

def setup(bot):
    bot.add_cog(DatabaseInfoInjector(bot))


