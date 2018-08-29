
class ErrorHandler:

    def __init__(self, bot):
        self.bot = bot

    @staticmethod
    async def on_command_error(ctx, exception):
        await ctx.send(f'{ctx} -> {exception}')

    @staticmethod
    async def on_error(event, *args, **kwargs):
        print(event, args, kwargs)


def setup(bot):
    bot.add_cog(ErrorHandler(bot))
