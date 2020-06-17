from discord.ext import commands
from discord import Embed
from aiohttp import ClientSession
from random import choice as c
from json import loads


async def get(session: object, url: object) -> object:
    async with session.get(url) as response:
        return await response.text()


async def reddit(sub: str):
    type = ['new', 'top', 'hot', 'rising']
    url = f"https://www.reddit.com/r/{sub}/{c(type)}.json?sort={c(type)}&limit=10"
    async with ClientSession() as session:
        data = await get(session, url)
        data = loads(data)
        data = data['data']['children']
        url = [d['data']['url'] for d in data]
        return c(url)


class Porn(commands.Cog):
    """NSFW content
    """

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.is_nsfw()
    async def milf(self, ctx):
        """
        Random images of milfs (NSFW)
        ?milf
        """
        url = await reddit(sub="milf")
        if not url.endswith('.jpg'):
            return await ctx.send(url)
        await ctx.send(embed=Embed(
            title="Milf", url=url
        ).set_image(url=url))

    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.is_nsfw()
    async def ass(self, ctx):
        """
        Random images of ass (NSFW)
        ?ass
        """
        url = await reddit(sub="ass")
        if not url.endswith('.jpg'):
            return await ctx.send(url)
        await ctx.send(embed=Embed(
            title="Ass", url=url
        ).set_image(url=url))

    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.is_nsfw()
    async def lesbians(self, ctx):
        """
        Random images of lesbians (NSFW)
        ?lesbians
        """
        url = await reddit(sub="lesbians")
        if not url.endswith('.jpg'):
            return await ctx.send(url)
        await ctx.send(embed=Embed(
            title="Lesbians", url=url
        ).set_image(url=url))


def setup(bot):
    bot.add_cog(Porn(bot))
