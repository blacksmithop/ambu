from discord.ext import commands
from discord import Embed
from random import randrange as r, choice as c
from datetime import datetime as dt
from aiohttp import ClientSession
from json import loads
from time import monotonic
import db


async def get(session: object, url: object) -> object:
    async with session.get(url) as response:
        return await response.text()


async def fetch(session: object, url: object) -> object:
    async with session.get(url) as response:
        url = await response.text()
        url = loads(url)
        url = url['data']['children']
        url = c(url)['data']
        return url


class Image(commands.Cog):
    """Image commands.
    """

    def __init__(self, bot):
        self.bot = bot
        self.db = db.BotConfig()

    @commands.command()
    async def ping(self, ctx):
        """
        Ping the bot
        ?ping
        """
        before = monotonic()
        await ctx.trigger_typing()
        after = monotonic()
        ms = int((after - before) * 1000)
        msg = await ctx.channel.send(f"```🏓 Ping: {ms} ms```")
        await msg.edit(content=f"{msg.content[:-3]}\n\n🤖 Latency: {int(self.bot.latency * 1000)} ms```")

    @commands.command()
    async def fox(self, ctx):
        """
        Get random fox images
        ?fox
        """
        url = f"https://randomfox.ca/images/{r(1, 122)}.jpg"
        await ctx.send(embed=Embed(
            title="🦊", timestamp=dt.now(), url=url
        ).set_image(url=url))

    @commands.command()
    async def dog(self, ctx):
        """
        Get random dog images
        ?dog
        """
        async with ClientSession() as session:
            url = await get(session, 'https://dog.ceo/api/breeds/image/random')
            url = loads(url)['message']
            await ctx.send(embed=Embed(
                title="🐩", timestamp=dt.now(), url=url
            ).set_image(url=url))

    @commands.command()
    async def cat(self, ctx):
        """
        Get random cat images
        ?cat
        """
        async with ClientSession() as session:
            url = await get(session, 'https://api.thecatapi.com/v1/images/search')
            url = loads(url)[0]['url']
            await ctx.send(embed=Embed(
                title="🐈", timestamp=dt.now(), url=url
            ).set_image(url=url))

    @commands.command()
    async def nature(self, ctx):
        """
        Get random nature images
        ?nature
        """
        async with ClientSession() as session:
            url = await fetch(session, 'https://www.reddit.com/r/earthporn/new.json?sort=hot&limit=40')
        await ctx.send(embed=Embed(
            title="🌳", timestamp=dt.now(), url=f"https://reddit.com/{url['permalink']}"
        ).set_image(url=url['url']))

    @commands.command()
    async def pics(self, ctx):
        """
        Get random images
        ?pics
        """
        async with ClientSession() as session:
            url = await fetch(session, 'https://www.reddit.com/r/pic/new.json?sort=hot&limit=40')
            await ctx.send(embed=Embed(
                title="🏕", timestamp=dt.now(), url=f"https://reddit.com/{url['permalink']}"
            ).set_image(url=url['url']))

    @commands.command(name='astro', aliases=['space'])
    async def astro(self, ctx):
        """
        Get random astronomy images
        ?astro
        """
        async with ClientSession() as session:
            url = await fetch(session, 'https://www.reddit.com/r/astrophotography/new.json?sort=hot&limit=40')
            await ctx.send(embed=Embed(
                title="🏕", timestamp=dt.now(), url=f"https://reddit.com/{url['permalink']}"
            ).set_image(url=url['url']))



def setup(bot):
    bot.add_cog(Image(bot))
