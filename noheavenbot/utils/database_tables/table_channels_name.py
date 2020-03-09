from noheavenbot.utils import Database


class TextChannels:

    @classmethod
    async def get_channels(cls):
        conn = await Database.connect()
        query = await conn.fetch('''
        SELECT nombre, identifier FROM nh.text_channels
        ''')

        return {nombre: identifier for nombre, identifier in query}

    def __new__(cls, *args, **kwargs):
        return cls.get_channels()
