from noheavenbot.utils import DatabaseConnection
from noheavenbot.utils.json_utils import Json
from discord.ext.commands import command


class DatabaseInfoInjector:
    def __init__(self, bot):
        self.bot = bot

    @command(name='use')
    async def get_users(self, ctx):
        conn = await DatabaseConnection.connect()
        for i, name in enumerate(Json.get('/home/surister/noheavenbot/noheavenbot/utils/garch.json')['name']):
            await conn.execute('''
            INSERT INTO garch (name, index) VALUES ($1, $2)
            ''', name, i)
        await conn.close()


def setup(bot):
    bot.add_cog(DatabaseInfoInjector(bot))

# DO ABOVE
