from discord.ext.commands import command


class Text:

    def __init__(self, bot):
        self.bot = bot

    @command()
    async def text(self, ctx, *, message):
        b = message.lower().replace("$text", "")
        a = b.split()
        for i in a:
            c = ""
            for k in i:
                c = c + ":regional_indicator_{}:".format(k)
            await ctx.send(c)
        await ctx.channel.delete_messages([ctx.message])


def setup(bot):

    bot.add_cog(Text(bot))
