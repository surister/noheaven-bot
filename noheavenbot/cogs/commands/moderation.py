from discord import Embed, Member
from discord.ext.commands import command, has_role, Cog

from noheavenbot.utils.constants import Fields
from noheavenbot.utils.constructors import EmbedConstructor
from noheavenbot.utils.validator import has_role as check_roles

# TOdo logs aqui en todo


def is_allowed(ctx):
    return ctx.author.id in (243742080223019019, 150726664760983552, 249482959357214720)
    # sur, alpha, drew


class Moderation(Cog):

    def __init__(self, bot):
        self.bot = bot

    # @check(is_allowed)
    # @command(name='reset')
    # async def bot_exit(self, ctx):
    #
    #     await ctx.send('Reiniciando..')
    #     try:
    #         self.bot.bot_disconnect.disconnect()
    #     except Exception as e:
    #         print(e)
    #     finally:
    #         exit(0)

    @command(name='help')
    async def command_for_help(self, ctx):

        # TODO better than this ''slicing'' system, is to separate both fields into admin_fields and user fields.
        # Revisit and rethink whole idea

        if check_roles('Server Admin', ctx.author.roles):
            help_embed = EmbedConstructor('Server commands', Fields.help_fields).construct()
        else:
            help_embed = EmbedConstructor('Server commands', Fields.help_fields[5:]).construct()
        await ctx.send(embed=help_embed)

    @command()
    async def music(self, ctx):
        help_embed = EmbedConstructor('Music commands', Fields.music_fields).construct()
        await ctx.send(embed=help_embed)

    @has_role('Server Admin')
    @command()
    async def perms(self, ctx, member: Member = None):

        if member is None:
            embed = Embed(title='__**Permissions**__')

            for perm in ctx.me.guild_permissions:
                if perm[1]:
                    embed.add_field(name=perm[0], value=':o:')
                else:
                    embed.add_field(name=perm[0], value=':x:')
            await ctx.send(embed=embed)
        else:
            embed = Embed(title='__**Permissions**__')

            for perm in member.guild_permissions:
                if perm[1]:
                    embed.add_field(name=perm[0], value=':o:')
                else:
                    embed.add_field(name=perm[0], value=':x:')
            await ctx.send(embed=embed)

    @command()
    async def info(self, ctx, *, user: Member):

        roles = [x.name for x in user.roles if x.name != "@everyone"]

        since_created = (ctx.message.created_at - user.created_at).days
        since_joined = (ctx.message.created_at - user.joined_at).days
        user_joined = user.joined_at.strftime("%d %b %Y %H:%M")
        user_created = user.created_at.strftime("%d %b %Y %H:%M")

        created_on = "{}\n({} days ago)".format(user_created, since_created)
        joined_on = "{}\n({} days ago)".format(user_joined, since_joined)

        game = "Chilling in {} status".format(user.status)

        if user.activity is None:
            pass

        else:
            game = "[{}]".format(user.activity.name)

        if roles:
            roles = sorted(roles, key=[x.name for x in ctx.guild.roles
                                       if x.name != "@everyone"].index)
            roles = ", ".join(roles)
        else:
            roles = "None"

        data = Embed(description=game, colour=user.colour)
        data.add_field(name="Joined Discord on", value=created_on)
        data.add_field(name="Joined this server on", value=joined_on)
        data.add_field(name="Roles", value=roles, inline=False)
        data.set_footer(text="User ID:{}".format(user.id))

        name = str(user)
        name = " ~ ".join((name, user.nick)) if user.nick else name

        if user.avatar_url:
            data.set_author(name=name, url=user.avatar_url)
            data.set_thumbnail(url=user.avatar_url)
        else:
            data.set_author(name=name)
        await ctx.send(embed=data)

    @command(name='d')
    @has_role('Server Admin')
    async def delete_messages(self, ctx, number: int):

        print(f'{ctx.message.author} deleted {number} messages in {ctx.channel}')
        mgs = [message async for message in ctx.channel.history(limit=number+1)]
        await ctx.channel.delete_messages(mgs)

    @command()
    async def ping(self, ctx):
        await ctx.send(f'Pong -> {self.bot.latency}')

    # TODO Make unique test file, not have it on moderation


    @command()
    async def test(self, ctx):
        await ctx.send(ctx.channel.is_nsfw())


def setup(bot):
    bot.add_cog(Moderation(bot))
