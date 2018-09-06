from discord import Embed


class ErrorHandler:

    def __init__(self, bot):
        self.bot = bot

    @staticmethod
    async def on_command_error(ctx, exception):
        embed = Embed(title=f' Error -> {exception}')
        await ctx.send(embed=embed)

    @staticmethod
    async def on_error(event, *args, **kwargs):
        print(event, args, kwargs)


def setup(bot):
    bot.add_cog(ErrorHandler(bot))
