from discord.ext import commands
from discord import Embed, Color
from aiohttp import ClientSession
from random import choice
from ast import literal_eval


async def get(session: object, url: object) -> object:
    async with session.get(url) as response:
        return await response.text()


class Photo(commands.Cog):
    """Search for photos.
    """

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='img')
    async def _image(self, ctx, *, query):
        image = Embed(color=Color.dark_teal())
        image.title = query.title()
        if len(query.split()) > 1:
            query = '+'.join(query.split())
        key = '17191614-063633dedf733f61470d1198b'
        base = f'https://pixabay.com/api/?key={key}&q={query}&lang=en&per_page=3'
        async with ClientSession() as session:
            url = await get(session, base)
        url = literal_eval(url)
        url = url['hits']
        url = choice(url)
        image.set_footer(text=url['tags'], icon_url="https://i.ibb.co/Vqgtj2z/pix.png")
        image.set_image(url=url['largeImageURL'])
        image.set_author(name=url['user'], icon_url=url['userImageURL'], url=url['pageURL'])
        await ctx.send(embed=image)


def setup(bot):
    bot.add_cog(Photo(bot))
