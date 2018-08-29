import os
from cogs.path import cogs_path

#Todo añadir logs en estas mierdas xd xd


class StartupExtension:

    blacklist = ['__pycache__', 'readme.txt', 'server_status.py', '__init__.py', 'path.py']

    @classmethod
    def to_array(cls):
        return [f'cogs.{cog}'.replace('.py', '') for cog in os.listdir(cogs_path) if cog not in
                                                                                        StartupExtension().blacklist]


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
