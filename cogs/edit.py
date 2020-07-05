from discord.ext import commands
from discord import Embed, Color, Member, File
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont
from urllib import request


class Edit(commands.Cog):
    """Image editing
    """

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def rip(self, ctx, vic: Member = None):
        if vic is None:
            vic = ctx.author
        url = "https://i.ibb.co/bNkKmz7/grave.png"
        file = BytesIO(request.urlopen(url).read())
        img = Image.open(file)
        draw = ImageDraw.Draw(img)
        font = ImageFont.truetype ("arial.ttf", 18)

        w, h = draw.textsize(vic.display_name)
        draw.text(((227-w)/2, (222-h)/2), vic.display_name, (0, 0, 0), font=font)
        img.save("rip.png")
        file = File("rip.png", filename="image.png")
        await ctx.send(file=file)


def setup(bot):
    bot.add_cog(Edit(bot))
