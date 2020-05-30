from discord.ext import commands
from discord import Embed
from random import randrange as r, choice as c
from datetime import datetime as dt
from aiohttp import ClientSession
from json import loads
from time import monotonic


async def fetch(session: object, url: object) -> object:
    async with session.get(url) as response:
        return await response.text()


class Image(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def ping(self, ctx):
        before = monotonic()
        await ctx.trigger_typing()
        after = monotonic()
        ms = int((after - before) * 1000)
        msg = await ctx.channel.send(f"```🏓 Ping: {ms} ms```")
        await ctx.trigger_typing()
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
            url = await fetch(session, 'https://dog.ceo/api/breeds/image/random')
            url = loads(url)['message']
            await ctx.send(embed=Embed(
                title="🐩", timestamp=dt.now(), url=url
            ).set_image(url=url))

    @commands.command()
    async def cat(self, ctx):
        async with ClientSession() as session:
            url = await fetch(session, 'https://api.thecatapi.com/v1/images/search')
            url = loads(url)[0]['url']
            await ctx.send(embed=Embed(
                title="🐈", timestamp=dt.now(), url=url
            ).set_image(url=url))

    @commands.command()
    async def nature(self, ctx):
        async with ClientSession() as session:
            url = await fetch(session, 'https://www.reddit.com/r/earthporn/new.json?sort=hot&limit=10')
            url = loads(url)
        url = url['data']['children']
        url = c(url)['data']
        await ctx.send(embed=Embed(
            title="🌳", timestamp=dt.now(), url=f"https://reddit.com/{url['permalink']}"
        ).set_image(url=url['url']))

    @commands.command()
    @commands.is_nsfw()
    async def porn(self, ctx):
        subs = ['NSFW_GIF', 'adorableporn', 'porn', 'nsfw', 'nsfw_gifs']
        subs = c(subs)
        async with ClientSession() as session:
            url = await fetch(session, f"https://www.reddit.com/r/{subs}/new.json?sort={c(['hot','top'])}&limit=30")
            url = loads(url)
        url = url['data']['children']
        url = c(url)['data']

        if not url['url'].endswith(('.jpg', '.gify', '.gif')):
            await ctx.send(url['url'])
            return
        await ctx.send(embed=Embed(
            title="👙", timestamp=dt.now(), url=f"https://reddit.com/{url['permalink']}"
        ).set_image(url=url['url']))


def setup(bot):
    bot.add_cog(Image(bot))
