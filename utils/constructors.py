from discord import Embed


class EmbedConstructor:

    __slots__ = ['title', 'fields']

    def __init__(self, title, *fields):
        self.title = title
        self.fields = fields

    def _construction(self):
        custom_embed = Embed(title=self.title)
        a, b, c = '', '', ''
        for different_field in self.fields:
            try:
                a, b = different_field
            except ValueError:
                c = different_field
            custom_embed.add_field(name=a, value=b, inline=False) if b is not None \
                else custom_embed.add_field(name=c, value='Empty', inline=False)
        return custom_embed

    def construct(self):
        return self._construction()
