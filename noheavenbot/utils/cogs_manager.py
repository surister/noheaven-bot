import os

from noheavenbot.utils.constants import Path

# Todo añadir logs en estas mierdas xd xd


class StartupExtension:

    blacklist = ['__pycache__', 'readme.txt', 'server_status.py', '__init__.py', 'path.py', '__pycache__.py',
                 'error_handler.py', 'sample-out.jpg', 'name_enforcer.py', 'playlist.json']

    @classmethod
    def to_array(cls):
        cog_list = []
        for element in os.listdir(Path.COGS):
            if element not in StartupExtension.blacklist:
                if os.path.isdir(f'{Path.COGS}/{element}'):
                    for cog in os.listdir(f'{Path.COGS}/{element}'):
                        if cog not in StartupExtension.blacklist:
                            cog_list.append(f'noheavenbot.cogs.{element}.{cog}'.replace('.py', ''))
                else:
                        cog_list.append(f'noheavenbot.cogs.{element}'.replace('py', ''))

        return cog_list


def load_cogs(instance):
    for extension in StartupExtension.to_array():
        try:
            instance.load_extension(extension)
        except Exception as e:
            exc = '{}: {}'.format(type(e).__name__, e)
            print('Failed to load extension {}\n{}'.format(extension, exc))


def unload_cogs(instance):
    for extension in StartupExtension.to_array():
        try:
            instance.unload_extension(extension)
        except Exception as e:
            print(e)
