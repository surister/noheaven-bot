from noheavenbot.utils.constants import TEXTCHANNELS, TRUSTED_BOTS

from noheavenbot.utils.database_tables import TextChannels
from noheavenbot.utils.database_tables import TrustedBot


class UpdateFromDataBase:
    """
    We update data from database such as TextChannels ids to be used.

    database_table.TextChannels -> UpdateFromDataBase (Updates dummy data class from
     .utils.constants -> Run in bot_ready.py
    """

    @classmethod
    async def update(cls):
        # TextChannels

        text_channels_query = await TextChannels().get_channels()
        for i, k in text_channels_query.items():
            TEXTCHANNELS.__setattr__(i, k)

        # Id to - do
        id_bot_query = await TrustedBot.get_ids()
        TRUSTED_BOTS.__setattr__('get_ids', id_bot_query)

    def __new__(cls, *args, **kwargs):
        return cls.update()
