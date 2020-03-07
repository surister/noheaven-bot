from discord.ext.commands import Cog
from asyncio import sleep


class OnMessage(Cog):

    def __init__(self, bot):
        self.bot = bot
        self.last = None

    @Cog.listener()
    async def on_message(self, message):
        if message.channel.id != 452527686506512384:

            if message.author.id == 234395307759108106:
                await message.channel.send(f"Tu {self.last.author.mention} de que coño vas, pon los comandos en {self.bot.get_channel(452527686506512384).mention}")
                await sleep(3)
                mgs = [message async for message in message.channel.history(limit=3)]
                await message.channel.delete_messages(mgs)

        self.last = message


def setup(bot):
    bot.add_cog(OnMessage(bot))
