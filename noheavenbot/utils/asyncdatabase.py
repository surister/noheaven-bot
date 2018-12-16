import asyncio

import asyncpg

from discord.ext.commands import command


class DatabaseMethods:
    @classmethod
    async def create_main_db(cls):
        conn = await asyncpg.connect('postgresql://postgres@localhost/surister')

        await conn.execute('''
            CREATE TABLE users(
                id serial PRIMARY KEY,
                name varchar(80),
                date date,
                admin boolean
            )
        ''')
