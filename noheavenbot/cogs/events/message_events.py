import json

from noheavenbot.utils.constants import Path
from discord.ext.commands import Cog


class OnMessage(Cog):
    def __init__(self, bot):
        self.bot = bot

    @staticmethod
    @Cog.listener()
    async def on_message(message):
        with open(f'{Path.UTILS}/muted.json', 'r') as f:
            x = json.load(f)
        if message.author.id in x['users']:
            await message.delete()
            await message.author.send('Estas muteado.')


def setup(bot):
    bot.add_cog(OnMessage(bot))
