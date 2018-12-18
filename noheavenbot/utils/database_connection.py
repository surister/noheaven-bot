from noheavenbot import Vars
from asyncpg import create_pool


class DatabaseConnection:

    @classmethod
    async def connect(cls):
        credentials = \
            {'user': 'root', 'password': Vars.dbpass, 'database': 'noheaven', 'host': 'localhost', 'port': '63333'}

        conn = await create_pool(**credentials)
        return conn


class DatabaseFunction:

    @classmethod
    async def insert_into_(cls, table: str):
        conn = await DatabaseConnection.connect()
        await conn.execute('''
        INSERT INTO $1 VALUES ()
        ''')

    @classmethod
    async def insert_garch(cls, name: str):
        conn = await DatabaseConnection.connect()
        await conn.execute('''
        INSERT INTO garch VALUES ($1) 
        ''', name)

    @classmethod
    async def fetch_garch(cls):
        conn = await DatabaseConnection.connect()
        await conn.fetchor

