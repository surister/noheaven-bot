import logging

try:
    from asyncpg import create_pool
except ModuleNotFoundError:
    logging.warning('Database not set up, install asyncpg')
from noheavenbot.utils.constants import EnvVariables


class DatabaseConnection:

    @classmethod
    async def connect(cls):
        credentials = {'user': 'root', 'password': EnvVariables.get('DBPASS'), 'database': 'noheaven',
                       'host': 'localhost', 'port': EnvVariables.get('PORT')}

        return await create_pool(**credentials)
