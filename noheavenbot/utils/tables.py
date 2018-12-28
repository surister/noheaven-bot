from random import randrange

from noheavenbot.utils import DatabaseConnection


class Garch:
    # https://stackoverflow.com/questions/38322870/select-table-and-column-dynamically-based-on-other-table-rows
    @classmethod
    async def get_max_index(cls):
        conn = await DatabaseConnection.connect()

        n = await conn.fetchval('''
        SELECT MAX(index) FROM garch
                        ''')

        await conn.close()
        return n

    @classmethod
    async def remove_row(cls, index: int):
        conn = await DatabaseConnection.connect()

        await conn.execute('''
        DELETE FROM garch where garch.index = $1
        ''', index)

    @classmethod
    async def insert_row(cls, name: str):
        conn = await DatabaseConnection.connect()

        await conn.execute('''
        INSERT INTO garch VALUES ($1, $2) 
        ''', name, await cls.get_max_index() + 1)

        await conn.close()

    @classmethod
    async def fetch_name(cls):
        n_rdm = randrange(0, await cls.get_max_index())
        conn = await DatabaseConnection.connect()

        name = await conn.fetchval('''
        SELECT name FROM garch WHERE index = $1
        ''', n_rdm)

        await conn.close()
        return name

    @classmethod
    async def fetch_all(cls):
        conn = await DatabaseConnection.connect()
        query = await conn.fetch('''
        SELECT * FROM garch''')

        return [f'{index}: {value}' for value, index in query]

