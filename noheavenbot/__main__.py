from asyncio import sleep

from discord import Game
from discord.ext.commands import Bot, when_mentioned_or

from noheavenbot.logger.bot_log import Log, Disconnecting
from noheavenbot.utils.cogs_manager import load_cogs
from noheavenbot.utils.login import Tokens

debug_mode = False


class bot(Bot):
    def __init__(self, prefix, status_name):

        super().__init__(
            command_prefix=when_mentioned_or(prefix),
            activity=Game(name=status_name))
        self.bg_task = self.loop.create_task(self.background_task())

    async def background_task(self):
        await self.wait_until_ready()

        member = self.get_guild(431125968455860224).get_member(150726664760983552)
        if member.nick != 'kowalski':
            await member.edit(nick='kowalski')
        await sleep(600)

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
