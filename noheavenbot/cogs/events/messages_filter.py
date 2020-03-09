from asyncio import sleep

from discord.ext.commands import Cog

from noheavenbot.utils.constants import TEXTCHANNELS


class OnMessage(Cog):

    def __init__(self, bot):
        self.bot = bot
        self.last = None

    @Cog.listener()
    async def on_message(self, message):
        bot_commands_channel = int(TEXTCHANNELS.get('comandos-bot'))

        if message.channel.id != bot_commands_channel:

            if message.author.id == 234395307759108106:  # id of current music bot, can change over time.
                await message.channel.send(f"Tu {self.last.author.mention} de que coño vas, pon los comandos en "
                                           f"{self.bot.get_channel(bot_commands_channel).mention}")
                await sleep(3)
                mgs = [message async for message in message.channel.history(limit=3)]
                await message.channel.delete_messages(mgs)

        self.last = message


def setup(bot):
    bot.add_cog(OnMessage(bot))
