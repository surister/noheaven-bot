from asyncio import sleep

from discord.ext.commands import Cog

from noheavenbot.utils.constants import TEXTCHANNELS, TRUSTED_BOTS


class OnMessage(Cog):

    def __init__(self, bot):
        self.bot = bot
        self.last = None

    @Cog.listener()
    async def on_message(self, message):
        bot_commands_channel = [int(TEXTCHANNELS.get('comandos-bot')), int(TEXTCHANNELS.get('bot-commands'))]

        if message.channel.id not in bot_commands_channel:
            if message.author.id in TRUSTED_BOTS.get_ids:  # id list of all trusted bots
                if message.content.startswith('Tu'):  # a bit hacky but works, saves us from having 2 bots
                    # or doing some other more complex logic
                    return

                await message.channel.send(f"Tu {self.last.author.mention} de que coño vas, pon los comandos en "
                                           f"{self.bot.get_channel(bot_commands_channel[0]).mention}")

                mgs = [message async for message in message.channel.history(limit=3)]

                await sleep(3)

                await message.channel.delete_messages(mgs)

        self.last = message


def setup(bot):
    bot.add_cog(OnMessage(bot))
