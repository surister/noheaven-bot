import asyncio

import asyncpg

from discord.ext.commands import command


class DatabaseInfoInjector:
    def __init__(self, bot):
        self.bot = bot

    @command()
    async def get_users(self, ctx):
        conn = await asyncpg.connect('postgresql://root@localhost/noheaven')
        async for member in ctx.guild.members:
            await conn.execute('''
            INSERT INTO users (id, name, date, admin) VALUES ($1, $2, $3, $4)
            ''', member.id, member.display_name, member.joined_at)
        await conn.close()
    print('finished')


def setup(bot):
    bot.add_cog(DatabaseInfoInjector(bot))
