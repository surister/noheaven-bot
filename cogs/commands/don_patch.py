import discord
from discord.ext import commands
from PIL import Image, ImageFont, ImageDraw
import io

from assets.don_patch.patch_path import path, font_path
from assets.don_patch.extra.welcome_image import welcome_img


def check_is_member(to_check: list):
    return all(map(lambda x: isinstance(x, discord.Member), to_check))


def beaten_img(w, l1, l2):
    img = Image.open(f"{path}/patch_beaten2.jpg")
    draw = ImageDraw.Draw(img)

    font = ImageFont.truetype(font_path, 25)
    # draw.text((x, y),"Sample Text",(r,g,b))
    draw.text((125, 5), w, (255, 255, 255), font=font)  # winner
    draw.text((215, 250), l1, (255, 255, 255), font=font)  # loser 1
    draw.text((310, 200), l2, (255, 255, 255), font=font)  # loser 2
    a = io.BytesIO()
    img.save(a, format='PNG')

    return a.getvalue()


class Patch:

    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['vencido'])
    async def beaten(self, ctx, user, l1, l2):

        await ctx.channel.trigger_typing()

        # if check_is_member([user, l1, l2]):

            # rb_file = beaten_img(user.display_name, l1.display_name, l2.display_name)
       # else:

        rb_file = beaten_img(user, l1, l2)

        await ctx.send(file=discord.File(rb_file, 'test.png'))


def setup(bot):
    bot.add_cog(Patch(bot))
