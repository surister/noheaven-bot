from discord.ext.commands import command, Cog
# from apexpy import ApexApi


class Text(Cog):

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

# class ApexLegend:
#     def __init__(self, bot):
#         self.bot = bot
#
#     @command()
#     async def apexsearch(self, ctx, name: str, platform:str):
#         player = ApexApi('4c4d90ce-e0b9-4696-9940-96da24b3b092')
#         await player.search(name, platform)
#         for legend in player.legends:
#             await ctx.send(legend.stats)


def setup(bot):
    # bot.add_cog(ApexLegend(bot))
    bot.add_cog(Text(bot))
