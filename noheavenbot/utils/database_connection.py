from asyncpg import create_pool

from noheavenbot.utils.constants import Vars


class DatabaseConnection:

    @classmethod
    async def connect(cls):
        credentials = \
            {'user': 'root', 'password': Vars.DBPASS, 'database': 'noheaven', 'host': 'localhost', 'port': '63333'}

        conn = await create_pool(**credentials)
        return conn
