import os

from typing import NamedTuple


class Vars(NamedTuple):
    try:
        debug_mode = os.environ['DEBUG_MODE']
    except KeyError:
        debug_mode = False

    prefix = '!' if not debug_mode else '%'
    token = os.environ['sur'] if debug_mode else os.environ['nhbot']
    database = 'surister' if debug_mode else 'noheaven'
    dbpass = os.environ['dbpasswd']
