from logger.bot_log import Log, Disconnecting

from discord import Game
from discord.ext.commands import Bot, when_mentioned_or


class bot(Bot):
    def __init__(self, prefix, status_name):

        super().__init__(
            command_prefix=when_mentioned_or(prefix),
            activity=Game(name=status_name),
        )

    @property
    def bot_log(self):
        return Log()
    @property
    def bot_disconnect(self):
        return Disconnecting


sur = bot('!', '!help -- para ayuda')

sur.run()

if sur.is_closed():
    try:
        sur.bot_disconnect.disconnect(sur)
    except Exception as e:
        print(e)
    finally:
        exit()
