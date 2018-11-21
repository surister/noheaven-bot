from typing import NamedTuple
from pathlib import PurePath


class Fields(NamedTuple):

    help_fields = (
                    ('__**Admins**__', 'Commands only avaliable for admins'),
                    ('!perms <user>', 'Shows the optional <users> permissions, ctx.author by default'),
                    ('!d <number>', 'Deletes <number> messages from the channel'),
                    ('!reload', 'Reloads cogs'),
                    ('!garch delete <indice>', 'Borra el nombre de garch de ese indice, los indices empiezan en 0'),
                    ('__**Users**__', 'Commands avaliable for every user'),
                    ('!info <user>', 'Shows <users> info'),
                    ('!ping', 'echo PONG'),
                    ('__**Nsfw**__', 'nsfw commands avaliable for every user'),
                    ('!porn <argument>', 'Sends an image of <argument> category'),
                    ('!porn list', 'Shows possible <argument>'),
                    ('!gif <argument>', 'Sends a gif of <argument> category'),
                    ('!gif list', 'Shows possible <argument>'),
                    ('!lol <argument', 'SEnds an image of <argument> category'),
                    ('!lol list', 'Shows possible <argument>'),
                    ('__**Garch**__', 'Garch commands'),
                    ('!garch', 'Shows a random garch name'),
                    ('!garch save <name>', 'Saves new garch name'),
                    ('!garch list', 'Shows the saved list')
                    )
    music_fields = (
        ('__**Musica**__', 'Comandos de musica'),
        ('!play <cancion>', 'Toca la <cancion>'),
        ('!next', 'Salta a la siguiente cancion, si no hay ninguna espera 60 segundos'),
        ('!stop', 'Cierra el bot')
        ('')
    )
    a = [
        ('test', 'boi'),
        ('test2', 'boi'),
        ('test3', 'running karma', 'running karma', 'running karma'),
        ('hok', ' boi'),
    ]

    nsfw_categories = [
        'amateur', 'anal', 'asian', 'ass', 'babes', 'bbw', 'bdsm', 'big', 'tits', 'blonde', 'blowjob',
        'brunette', 'celebrity', 'college', 'creampie', 'cumshots', 'double', 'penetration', 'ebony',
        'emo', 'female-ejaculation', 'fisting', 'footjob', 'gangbang', 'gay', 'girlfriend', 'group',
        'sex', 'hairy', 'handjob', 'hardcore', 'hentai', 'indian', 'interracial', 'latina', 'lesbian',
        'lingerie', 'masturbation', 'mature', 'milf', 'non-nude', 'panties', 'penis', 'pornstar', 'public',
        'sex', 'pussy', 'redhead', 'self', 'shot', 'shemale', 'teen', '(18+)', 'threesome', 'toys'
    ]

    nsfw_lol = [
        'ahri', 'akali', 'anivia', 'annie', 'ashe', 'caitlyn',
        'camille', 'cassiopeia', 'diana', 'elise', 'evelynn',
        'fiora', "kai'sa", 'kalista', 'karma', 'katarina',
        'kayle', 'kindred', 'leblanc', 'leona', 'lissandra',
        'lulu', 'lux', 'missfortune', 'morgana', 'nami', 'nidalee',
        'oriana', 'poppy', 'quinn', "rek'sai", 'riven', 'sejuani',
        'shyvana', 'sivir', 'sona', 'soraka', 'syndra', 'taliyah',
        'tristana', 'vayne', 'vi', 'xayah', 'zoe', 'zyra', 'group',
        'cosplay', 'genderbender', 'male', 'irelia', 'jinx', 'random or r'
                ]

    nsfw_conversion = {
        'conversion_index': ['taliya', 'camille', "kai'sa", "rek'sai", 'zoe', 'xayah'],
        'taliyah': '360-taliya',
        'camille': '363-camille',
        "kai'sa": '374-kai_sa',
        "rek'sai": '256-rek_sai',
        'zoe': '373-zoe',
        'xayah': '370-xayah'
    }


class Path(NamedTuple):

    _NOHEAVEN_BASE = str(PurePath(__file__).parent)
    _NOHEAVEN = _NOHEAVEN_BASE.replace('utils', '')

    UTILS = _NOHEAVEN_BASE
    COGS = f'{_NOHEAVEN}cogs/'

    COMMANDS = f'{COGS}commands/'
    EVENTS = f'{COGS}events/'




