from discord.ext import commands
from discord import Embed, Color, Member, File
from io import BytesIO
from PIL import Image, ImageDraw, ImageOps
from urllib import request
from aiohttp import ClientSession


async def get(session: object, url: object) -> object:
    async with session.get(url) as response:
        return await response.read()


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

        w, h = draw.textsize(vic.display_name)
        draw.text(((227-w)/2, (222-h)/2), vic.display_name, (0, 0, 0))
        arr = BytesIO()
        img.save(arr, format='PNG')
        arr.seek(0)
        file = File(arr, filename="rip.png")
        await ctx.send(file=file)

    @commands.command()
    async def invert(self, ctx, vic: Member = None):
        if vic is None:
            vic = ctx.author
        url = str(vic.avatar_url_as(format="png"))
        async with ClientSession() as session:
            url = await get(session, url)
        file = BytesIO(url)
        img = Image.open(file)
        img = ImageOps.invert(img.convert('RGB'))
        arr = BytesIO()
        img.save(arr, format='PNG')
        arr.seek(0)
        file = File(arr, filename="rip.png")
        await ctx.send(file=file)

    @commands.command(name='avatar', aliases=['av'])
    async def avatar(self, ctx, m: Member = None):
        return await ctx.send(embed=Embed(color=m.color, title=m.display_name).set_image(url=m.avatar_url))


def setup(bot):
    bot.add_cog(Edit(bot))
