from PIL import Image, ImageFont, ImageDraw, ImageOps
import io
from noheavenbot.assets.don_patch import font_path
import os

path = os.path.dirname(__file__)

# TODO variable naming is horrendous, change pathing from `os` to `pathlib`


def welcome_img(user: str):

    im = Image.open(f"{path}/t.png")

    #  User name text
    font = ImageFont.truetype(font_path, 150)
    txt = Image.new('L', (600, 400))
    d = ImageDraw.Draw(txt)
    d.text((0, 0), user,  font=font, fill=255)
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
