import discord
from discord.ext.commands import command, Cog

from noheavenbot.utils.image_manipulation import beaten_img


def check_is_member(to_check: list):
    return all(map(lambda x: isinstance(x, discord.Member), to_check))


class DonPatch(Cog):
    def __init__(self, bot):
        self.bot = bot

    @command(aliases=['vencido'])
    async def beaten(self, ctx, user, l1, l2):

        await ctx.channel.trigger_typing()
        await ctx.send(file=discord.File(beaten_img(user, l1, l2), 'beaten.png'))


def setup(bot):
    bot.add_cog(DonPatch(bot))
