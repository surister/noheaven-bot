from discord import Game
from discord.ext.commands import Bot, when_mentioned_or

from noheavenbot.logger.bot_log import Log, Disconnecting
from noheavenbot.utils.cogs_manager import load_cogs
from noheavenbot.utils.constants import Vars


class CustomBot(Bot):
    def __init__(self, prefix, status_name):

        super().__init__(command_prefix=when_mentioned_or(prefix), activity=Game(name=status_name))

    @property
    def bot_log(self):
        return Log()

    @property
    def bot_disconnect(self):
        return Disconnecting


noheaven_bot = CustomBot(Vars.PREFIX, '!help -- para ayuda')
noheaven_bot.remove_command('help')

if __name__ == '__main__':
    load_cogs(noheaven_bot)
    noheaven_bot.run(Vars.TOKEN)

    if noheaven_bot.is_closed():
        try:
            noheaven_bot.bot_disconnect.disconnect()
        except Exception as e:
            print(e)
        finally:
            exit()
