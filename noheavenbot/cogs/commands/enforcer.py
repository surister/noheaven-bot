from discord.ext.commands import command
"""
    async def background_task(self):
        await self.wait_until_ready()
        # Todo delete this
        # This is just memery, ignore it.
        member = self.get_guild(431125968455860224).get_member(150726664760983552)
        if member.nick != 'kowalski':
            await member.edit(nick='kowalski')
        await sleep(600)
"""


class Name:
    def __init__(self, bot):
        self.bot = bot



class Role:
    pass