from PIL import Image, ImageFont, ImageDraw, ImageOps
import io
from assets.don_patch.patch_path import font_path
import os

path = os.path.dirname(__file__)


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
    font2 = ImageFont.truetype(font_path, 150)
    txt = Image.new('L', (600, 500))
    d = ImageDraw.Draw(txt)
    d.text((0, 0), "NoHeaven",  font=font2, fill=255)
    w = txt.rotate(23,  expand=1)

    im.paste(ImageOps.colorize(w, (0, 0, 0), (0, 0, 0)), (1400, 250),  w)

    pe = im.resize((1300, 1000))
    a = io.BytesIO()
    pe.save(a, format='PNG')

    return a.getvalue()
