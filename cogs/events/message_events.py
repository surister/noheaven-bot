import json

from utils.path import utils_path


class OnMessage:
    def __init__(self, bot):
        self.bot = bot

    @staticmethod
    async def on_message(message):
        with open(f'{utils_path}/muted.json', 'r') as f:
            x = json.load(f)
        if message.author.id in x['users']:
            await message.delete()


def setup(bot):
    bot.add_cog(OnMessage(bot))
