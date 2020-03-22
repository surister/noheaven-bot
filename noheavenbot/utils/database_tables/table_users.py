from noheavenbot.utils import Database


class Users:

    @classmethod
    async def len(cls):
        conn = await Database.connect()
        query = await conn.fetch('''
        SELECT COUNT(*) FROM nh.users
        ''')

        return query[0][0]

    @classmethod
    async def insert_single(cls, nombre: str, is_boot: bool, discriminator: int, identifier: str):
        conn = await Database.connect()
        await conn.execute('''
        INSERT INTO nh.users_test (id, nombre_actual, is_bot, name_identifier, identifier) VALUES (DEFAULT, $1, $2, $3, $4)
        
        ''', nombre, is_boot, discriminator, identifier)

    @classmethod
    async def insert_many(cls, values):
        conn = await Database.connect()
        await conn.executemany('''
        INSERT INTO nh.users (id, nombre_actual, is_bot, name_identifier, identifier) VALUES (DEFAULT, $1, $2, $3, $4)

        ''', values)

    @classmethod
    async def get_users_identifiers_list(cls):
        conn = await Database.connect()
        query = await conn.fetch('''
                SELECT identifier FROM nh.users
                ''')
        ids = [i[0] for i in query]

        return ids

    @classmethod
    async def update(cls, users: dict):
        if len(users) > await cls.len():
            for user in users:
                pass




