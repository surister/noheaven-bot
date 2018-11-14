import logging
import os

from shutil import copy
from time import strftime

bot_log_path = f'{os.path.dirname(__file__)}/log - {strftime("%y %m %d")}.log'
bot_log_folder = f'{os.path.dirname(__file__)}/logs'
asd = f'{os.path.dirname(__file__)} asdf.txt'


def prettier_msg(*args):
    return f' {strftime("%y %m %d")} -> {args}'


class Log:
    logging.basicConfig(filename=bot_log_path, level=logging.DEBUG)

    @classmethod
    def write(cls, *msg):
        return logging.info(prettier_msg(msg))

    @classmethod
    def warning(cls, *msg):
        logging.warning(prettier_msg(msg))


class Disconnecting:

    @classmethod
    def disconnect(cls):
        Log.warning('Disconecting')

        copy(bot_log_path, bot_log_folder)

        os.remove(bot_log_path)
