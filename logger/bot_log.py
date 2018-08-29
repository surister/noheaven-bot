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
        return logging.info(custom_msg(msg))

    @classmethod
    def warning(cls, *msg):
        logging.warning(custom_msg(msg))


class Disconnecting:

    @classmethod
    def disconnect(cls, instance):
        Log.warning('Disconecting')
        instance.http_sesion.close()

        copy(bot_log_path, bot_log_folder)

        os.remove(bot_log_path)

