import logging

try:
    from asyncpg import create_pool
except ModuleNotFoundError:
    logging.warning('Database not set up, install asyncpg')

from noheavenbot.utils.constants import EnvVariables


class Database:

    @classmethod
    async def connect(cls):
        credentials = {'user': EnvVariables.get('DB_USER'),
                       'password': EnvVariables.get('DB_PASS'),
                       'database': EnvVariables.get('DB_DATABASE'),
                       'host': EnvVariables.get('DB_HOST'),
                       'port': EnvVariables.get('DB_PORT')}

        return await create_pool(**credentials)
