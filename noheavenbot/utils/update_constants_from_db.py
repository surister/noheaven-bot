from noheavenbot.utils.constants import TEXTCHANNELS

from noheavenbot.utils.database_tables import TextChannels


class UpdateFromDataBase:
    """
    We update data from database such as TextChannels ids to be used.

    database_table.TextChannels -> UpdateFromDataBase (Updates dummy data class from
     .utils.constants -> Run in bot_ready.py
    """

    @classmethod
    async def update(cls):
        # TextChannels

        query = await TextChannels()
        for i, k in query.items():
            TEXTCHANNELS.__setattr__(i, k)

        # Id to - do

    def __new__(cls, *args, **kwargs):
        return cls.update()
