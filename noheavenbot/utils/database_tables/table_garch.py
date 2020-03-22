from random import randrange

from noheavenbot.utils import Database


class Garch:
    # https://stackoverflow.com/questions/38322870/select-table-and-column-dynamically-based-on-other-table-rows
    @classmethod
    async def get_max_index(cls):
        conn = await Database.connect()

        n = await conn.fetchval('''
        SELECT COUNT(*) FROM nh.garch_names
                        ''')

        await conn.close()
        return n

    @classmethod
    async def remove_row(cls, index: int):
        conn = await Database.connect()

        await conn.execute('''
        DELETE FROM nh.garch_names WHERE nh.garch_names.id=$1
        ''', index)

    @classmethod
    async def insert_row(cls, name: str):
        conn = await Database.connect()

        await conn.execute('''
        INSERT INTO nh.garch_names VALUES (DEFAULT, $1)
        ''', name)

        await conn.close()

    @classmethod
    async def fetch_name(cls):
        n_rdm = randrange(0, await cls.get_max_index())
        conn = await Database.connect()

        name = await conn.fetchval('''
        SELECT name FROM nh.garch_names WHERE id = $1
        ''', n_rdm)

        await conn.close()
        return name

    @classmethod
    async def fetch_all(cls):
        conn = await Database.connect()
        query = await conn.fetch('''
        SELECT * FROM nh.garch_names''')

        return [f'{index}: {value}' for value, index in query]

