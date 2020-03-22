from discord import File
from discord.utils import get
from discord.ext.commands import Cog

from noheavenbot.utils.image_manipulation import welcome_img
from noheavenbot.utils.database_tables.table_users import Users


class OnMemberActions(Cog):

    def __init__(self, bot):
        super().__init__()
        self.bot = bot

    @Cog.listener()
    async def on_member_join(self, member):
        channel = self.bot.get_channel(452530575618867200)

        role = get(member.guild.roles, name='Friends')
        await member.add_roles(role)
        await channel.purge(limit=2)
        name = f'{member.display_name[:8]}.' if len(member.display_name) >= 9 else member.display_name
        await channel.send(f'Bienvenido {member.mention} a {member.guild.name} ',
                           file=File(welcome_img(name), 'welcome.png'))

        await Users.insert_single(member.name, member.bot, int(member.discriminator), str(member.id))


def setup(bot):
    bot.add_cog(OnMemberActions(bot))
