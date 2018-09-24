from discord import Game
from discord.ext.commands import Bot, when_mentioned_or

from logger.bot_log import Log, Disconnecting
from utils.cogs_manager import load_cogs
from utils.login import Tokens

debug_mode = False


class bot(Bot):
    def __init__(self, prefix, status_name):

        super().__init__(
            command_prefix=when_mentioned_or(prefix),
            activity=Game(name=status_name))

    @property
    def bot_log(self):
        return Log()

    @property
    def bot_disconnect(self):
        self.http.close()
        return Disconnecting


_bot = bot('!' if not debug_mode else 'b', '!help -- para ayuda')
_bot.remove_command('help')

if __name__ == '__main__':

    load_cogs(_bot)

    _bot.run(Tokens.sur if debug_mode else Tokens.nhbot)

    if _bot.is_closed():
        try:
            _bot.bot_disconnect.disconnect()
        except Exception as e:
            print(e)
        finally:
            exit()
