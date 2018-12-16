from os import environ
from noheavenbot import Vars
from asyncpg import create_pool


class DatabaseConnection:

    @classmethod
    async def connect(cls):

        credentials = {'users': 'root', 'password': environ['dbpasswd'], 'database': Vars.database, 'host': '127.0.0.1'}
        db = await create_pool(**credentials)
        print(dir(db))
        return db
