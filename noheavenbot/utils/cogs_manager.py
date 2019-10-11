import os

from noheavenbot.utils.constants import Path

# Todo añadir logs en estas mierdas xd xd
# Todo Cambiar os pathing a pathlib


class CogList:

    blacklist = ['__pycache__', 'readme.txt', 'server_status.py', '__init__.py', 'path.py', '__pycache__.py',
                 'error_handler.py', 'sample-out.jpg', 'name_enforcer.py', 'playlist.json']

    @classmethod
    def get(cls) -> list:
        cog_list = []
        for element in os.listdir(Path.COGS):
            if element not in CogList.blacklist:
                if os.path.isdir(f'{Path.COGS}/{element}'):
                    for cog in os.listdir(f'{Path.COGS}/{element}'):
                        if cog not in CogList.blacklist:
                            cog_list.append(f'noheavenbot.cogs.{element}.{cog}'.replace('.py', ''))
                else:
                    cog_list.append(f'noheavenbot.cogs.{element}'.replace('py', ''))
        return cog_list

    def __new__(cls, *args, **kwargs):
        return cls.get()


def load_cogs(instance):
    for extension in CogList():
        try:
            instance.load_extension(extension)
        except Exception as e:
            exc = '{}: {}'.format(type(e).__name__, e)
            print('Failed to load extension {}\n{}'.format(extension, exc))


def unload_cogs(instance):
    for extension in CogList():
        try:
            instance.unload_extension(extension)
        except Exception as e:
            print(e)
