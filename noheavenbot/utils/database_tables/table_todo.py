from random import randrange

from noheavenbot.utils import Database


class Todo:
    # https://stackoverflow.com/questions/38322870/select-table-and-column-dynamically-based-on-other-table-rows
    @classmethod
    async def get_max_index(cls):
        conn = await Database.connect()

        n = await conn.fetchval('''
        SELECT MAX(id) FROM nh.todo
                        ''')

        await conn.close()
        return n

    @classmethod
    async def remove_row(cls, index: int):
        conn = await Database.connect()

        await conn.execute('''
        DELETE FROM nh.todo WHERE nh.todo.id=$1
        ''', index)

    @classmethod
    async def insert_row(cls, text: str):
        conn = await Database.connect()

        await conn.execute('''
        INSERT INTO nh.todo VALUES (DEFAULT, $1)
        ''', text)

        await conn.close()

    @classmethod
    async def fetch_all(cls, uncompleted=False):
        conn = await Database.connect()
        if uncompleted:

            query = await conn.fetch('''
            SELECT * FROM nh.todo ORDER BY nh.todo.finished ASC''')

        return [f'{index}: {value} : status {done}' for value, index, done in query]

    @classmethod
    async def set_completed(cls, n: int):
        conn = await Database.connect()
        await conn.execute('''
            UPDATE nh.todo SET finished = true WHERE nh.todo.id = $1
            
            ''', n)

    @classmethod
    async def move_away(cls, n: int):
        conn = await Database.connect()

        await conn.execute('''
        INSERT INTO nh.todo_finished (id, text, finished)
         VALUES (SELECT id, text, finished FROM nh.todo WHERE nh.todo.id = $1 )
        ''', n)
        await cls.remove_row(n)
