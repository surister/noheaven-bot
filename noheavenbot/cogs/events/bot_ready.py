from time import strftime
from discord.ext.commands import Cog
import logging


class Ready(Cog):

    def __init__(self, bot):
        super().__init__()
        self.bot = bot

    @Cog.listener()
    async def on_ready(self):
        s = '\n----------------------------\n'
        fmt = "Conectado como: {0} \n Id: {1} \n {2}".format(
            self.bot.user.name,
            self.bot.user.id,
            strftime("%c"))
        finalstr = f'{s} {fmt} {s}'
        logging.log(logging.INFO, finalstr)


def setup(bot):
    bot.add_cog(Ready(bot))
