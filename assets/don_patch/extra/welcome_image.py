from PIL import Image, ImageFont, ImageDraw, ImageOps
import io
from assets.don_patch.patch_path import font_path


def welcome_img(user: str):

    im = Image.open("/home/surister/noheavenbot/assets/don_patch/extra/t.png")

    #  User name text
    font = ImageFont.truetype(font_path, 50)
    txt = Image.new('L', (500, 50))
    d = ImageDraw.Draw(txt)
    d.text((0, 0), user,  font=font, fill=255)
    w = txt.rotate(17.5,  expand=1)

    im.paste(ImageOps.colorize(w, (0, 0, 0), (0, 0, 0)), (950, 1100),  w)

    # NoHeaven name text
    font2 = ImageFont.truetype(font_path, 55)
    txt = Image.new('L', (500, 500))
    d = ImageDraw.Draw(txt)
    d.text((0, 0), "NoHeaven",  font=font2, fill=255)
    w = txt.rotate(25,  expand=1)

    im.paste(ImageOps.colorize(w, (0, 0, 0), (0, 0, 0)), (1500, 250),  w)
    a = io.BytesIO()
    im.save(a, format='PNG')
    return a.getvalue()
