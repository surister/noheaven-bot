from discord import Game
from discord.ext.commands import Bot, when_mentioned_or


from noheavenbot.utils.cogs_manager import load_cogs
from noheavenbot.utils.constants import EnvVariables

from time import strftime
import logging

logging.basicConfig(level=logging.INFO)


def get_prefix(bot, msg):
    prefix = ['!']
    return when_mentioned_or(*prefix)(bot, msg)


def warning(msg):
    return logging.warning(f'Warning at {strftime("%c")} in {__file__} -> {msg}')


bot = Bot(command_prefix=get_prefix, activity=Game(name='!help -- para ayuda'))
bot.remove_command('help')
bot.warning = warning

if __name__ == '__main__':
    load_cogs(bot)
    bot.run(EnvVariables.get('token'))
