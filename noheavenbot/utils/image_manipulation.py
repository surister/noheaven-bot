from PIL import Image, ImageFont, ImageDraw, ImageOps
import io
from noheavenbot.utils.constants import Path

welcome_img_path = Path.ASSETS_FOLDER + '/castle.png'
font_path = Path.ASSETS_FOLDER + '/impact.ttf'
don_patch_beaten_path = Path.IMGS_FOLDER + '/patch_beaten2.jpg'
# TODO variable naming is horrendous


def welcome_img(user_name: str):

    im = Image.open(welcome_img_path)

    #  User name text
    font = ImageFont.truetype(font_path, 150)
    txt = Image.new('L', (600, 400))
    d = ImageDraw.Draw(txt)
    d.text((0, 0), user_name,  font=font, fill=255)
    w = txt.rotate(17.5,  expand=1)

    im.paste(ImageOps.colorize(w, (0, 0, 0), (0, 0, 0)), (750, 1000),  w)

    # NoHeaven name text

    txt = Image.new('L', (600, 500))
    d = ImageDraw.Draw(txt)
    d.text((0, 0), "NoHeaven",  font=font, fill=255)
    w = txt.rotate(23,  expand=1)

    im.paste(ImageOps.colorize(w, (0, 0, 0), (0, 0, 0)), (1400, 250),  w)

    pe = im.resize((1300, 1000))

    a = io.BytesIO()
    pe.save(a, format='PNG')
    a.seek(0)  # this line fixed errors that did not exist before, got from
               # https://gist.github.com/Gorialis/e89482310d74a90a946b44cf34009e88
               # Have a look at this.

    return a

# TODO Variable namig please, beating_img func


def beaten_img(winner, loser_1, loser_2):
    base_image = Image.open(don_patch_beaten_path)  # See image to understand function
    draw = ImageDraw.Draw(base_image)

    font = ImageFont.truetype(font_path, 25)
    # draw.text((x, y),"Sample Text",(r,g,b))
    draw.text((125, 5), winner, (255, 255, 255), font=font)
    draw.text((215, 250), loser_1, (255, 255, 255), font=font)
    draw.text((310, 200), loser_2, (255, 255, 255), font=font)
    buffer = io.BytesIO()
    base_image.save(buffer, format='PNG')
    buffer.seek(0)  # We set the offset position to 0, otherwise we get bye offsets errors.
    return buffer

