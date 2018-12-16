import asyncio

import asyncpg


class DatabaseMethods:
    @classmethod
    async def create_main_db(cls):
        conn = await asyncpg.connect('postgresql://postgres@localhost/surister')

        await conn.execute('''
            CREATE TABLE users(
                id BIGINT PRIMARY KEY,
                name varchar(32),
                date date,
                admin boolean
            )
        ''')


asyncio.get_event_loop().run_until_complete(DatabaseMethods.create_main_db())
