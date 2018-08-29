from time import strftime


class Ready:

    def __init__(self, bot):
        self.bot = bot

    async def on_ready(self):
        self.bot.bot_log.write('Bot is connected')
        s = '\n----------------------------\n'
        fmt = "Conectado como: {0} \n Id: {1} \n {2}".format(
            self.bot.user.name,
            self.bot.user.id,
            strftime("%c"))
        print(s, fmt, s)


def setup(bot):
    bot.add_cog(Ready(bot))
