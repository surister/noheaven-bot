from random import randrange

from noheavenbot.utils import DatabaseConnection


class Table:
    tables = ['garch']
    table = None

    if table is not None:
        if table not in tables:
            raise Exception('Check tables')

    @classmethod
    async def get_max_index(cls):
        conn = await DatabaseConnection.connect()
        n = await conn.fetchval('''
        SELECT MAX(index) FROM $1
                        ''', cls.table)
        await conn.close()

        return n

    @classmethod
    async def remove_row(cls, index: int):
        conn = await DatabaseConnection.connect()
        conn.execute('''
        DELETE FROM $2 where $2.index = $1
        ''', index, cls.table)

    @classmethod
    async def insert_row(cls, name: str):
        conn = await DatabaseConnection.connect()
        await conn.execute('''
        INSERT INTO $3 VALUES ($1, $2) 
        ''', name, await GarchTable.get_max_index() + 1, cls.table)

        await conn.close()

    @classmethod
    async def fetch_name(cls):
        n_rdm = randrange(0, await GarchTable.get_max_index())
        conn = await DatabaseConnection.connect()

        name = await conn.fetchval('''
        SELECT name FROM $2 WHERE index = $1
        ''', n_rdm, cls.table)
        await conn.close()
        return name

    @classmethod
    async def fetch_all(cls):
        conn = await DatabaseConnection.connect()
        query = await conn.fetch('''
        SELECT * FROM $1''', cls.table)

        return [f'{index}: {value}' for value, index in query]


class GarchTable(Table):
    table = 'garch'

