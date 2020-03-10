from discord.ext.commands import command, Cog


class Text(Cog):

    def __init__(self, bot):
        self.bot = bot

    @command(aliases=['t'])
    async def text(self, ctx, *, message):

        message_splitted = message.split()
        for word in message_splitted:
            c = ""
            for char in word:
                c = c + f":regional_indicator_{char}:"
            await ctx.send(c)
        await ctx.channel.delete_messages([ctx.message])


def setup(bot):
    # bot.add_cog(ApexLegend(bot))
    bot.add_cog(Text(bot))
