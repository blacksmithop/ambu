from discord.ext import commands
from discord import Embed
from random import randrange as r, choice as c
from datetime import datetime as dt
from aiohttp import ClientSession
from json import loads
from time import monotonic
from os import getenv as e


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

    @commands.command()
    async def ping(self, ctx):
        before = monotonic()
        await ctx.trigger_typing()
        after = monotonic()
        ms = int((after - before) * 1000)
        msg = await ctx.channel.send(f"```🏓 Ping: {ms} ms```")
        await msg.edit(content=f"{msg.content[:-3]}\n\n🤖 Latency: {int(self.bot.latency * 1000)} ms```")

    @commands.command()
    async def fox(self, ctx):
        url = f"https://randomfox.ca/images/{r(1, 122)}.jpg"
        await ctx.send(embed=Embed(
            title="🦊", timestamp=dt.now(), url=url
        ).set_image(url=url))

    @commands.command()
    async def dog(self, ctx):
        async with ClientSession() as session:
            url = await get(session, 'https://dog.ceo/api/breeds/image/random')
            url = loads(url)['message']
            await ctx.send(embed=Embed(
                title="🐩", timestamp=dt.now(), url=url
            ).set_image(url=url))

    @commands.command()
    async def cat(self, ctx):
        async with ClientSession() as session:
            url = await get(session, 'https://api.thecatapi.com/v1/images/search')
            url = loads(url)[0]['url']
            await ctx.send(embed=Embed(
                title="🐈", timestamp=dt.now(), url=url
            ).set_image(url=url))

    @commands.command()
    async def nature(self, ctx):
        async with ClientSession() as session:
            url = await fetch(session, 'https://www.reddit.com/r/earthporn/new.json?sort=hot&limit=40')
        await ctx.send(embed=Embed(
            title="🌳", timestamp=dt.now(), url=f"https://reddit.com/{url['permalink']}"
        ).set_image(url=url['url']))

    @commands.command()
    @commands.is_nsfw()
    async def porn(self, ctx):
        subs = ['NSFW_GIF', 'adorableporn', 'porn', 'nsfw', 'nsfw_gifs']
        subs = c(subs)
        async with ClientSession() as session:
            url = await fetch(session, f"https://www.reddit.com/r/{subs}/new.json?sort={c(['hot', 'top'])}&limit=30")
            url = loads(url)
        url = url['data']['children']
        url = c(url)['data']

        if not url['url'].endswith(('.jpg', '.gify', '.gif')):
            await ctx.send(url['url'])
            return
        await ctx.send(embed=Embed(
            title="👙", timestamp=dt.now(), url=f"https://reddit.com/{url['permalink']}"
        ).set_image(url=url['url']))

    @commands.command()
    async def pics(self, ctx):
        async with ClientSession() as session:
            url = await fetch(session, 'https://www.reddit.com/r/pic/new.json?sort=hot&limit=40')
            await ctx.send(embed=Embed(
                title="🏕", timestamp=dt.now(), url=f"https://reddit.com/{url['permalink']}"
            ).set_image(url=url['url']))

    @commands.command()
    async def astro(self, ctx):
        async with ClientSession() as session:
            url = await fetch(session, 'https://www.reddit.com/r/astrophotography/new.json?sort=hot&limit=40')
            await ctx.send(embed=Embed(
                title="🏕", timestamp=dt.now(), url=f"https://reddit.com/{url['permalink']}"
            ).set_image(url=url['url']))

    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def snap(self, ctx, url):
        base = "https://image.thum.io/get/width/600/crop/600/"
        if 'https://' not in url:
            url = f"https://{url}"
        link = f"{base}{url}"
        print(link)
        await ctx.send(embed=Embed().set_image(url=link))

    @commands.command()
    @commands.cooldown(1, 5)
    async def random(self, ctx):
        base = "https://api.unsplash.com/photos/random/?client_id="
        client = e("unsp_acc").split(';')
        link = f"{base}{c(client)}"
        async with ClientSession() as session:
            url = await get(session, link)
            url = loads(url)['urls']['regular']
            await ctx.send(embed=Embed().set_image(url=url))


def setup(bot):
    bot.add_cog(Image(bot))
