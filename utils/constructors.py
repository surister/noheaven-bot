from discord import Embed


class EmbedConstructor:

    __slots__ = ['title', 'fields', 'n']

    def __init__(self, title, n=0, *fields):

        self.title = title

        self.n = n
        self.fields = fields[0][self.n:]

    def _construction(self):
        custom_embed = Embed(title=self.title)

        for different_field in self.fields:
            if len(different_field) == 2:
                if any(map(lambda x: x.lower() == 'empty', different_field)):
                    if different_field.index('Empty') == 0:
                        custom_embed.add_field(name='\u200b', value=different_field[1], inline=False)
                    else:
                        custom_embed.add_field(name=different_field[0], value='\u200b', inline=False)
                else:
                    custom_embed.add_field(name=different_field[0], value=different_field[1], inline=False)
            else:
                custom_embed.add_field(name=different_field, value='\u200b', inline=False)

        return custom_embed

    def construct(self):
        return self._construction()
