from discord.ext import commands
from discord import Embed, Color
from aiohttp import ClientSession
from ast import literal_eval
from random import randrange
from json import loads
from urllib.request import urlopen


async def get(session: object, url: object) -> object:
    async with session.get(url) as response:
        return await response.text()


class Rates(commands.Cog):
    """Conversion
    """

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='er', aliases=['exchange'])
    async def er(self, ctx, c1: str = 'INR'):
        c1 = c1.upper()
        base = f"https://api.ratesapi.io/api/latest?base={c1}"
        async with ClientSession() as session:
            data = await get(session, base)
        data = literal_eval(data)
        if 'error' in data:
            return await ctx.send(f"{c1} is not a valid Currency")
        rate = Embed(color=Color.blurple())
        rate.title = f"Exchange rate for {c1}"
        data = data['rates']
        for c in ['USD', 'GBP', 'HKD', 'AUD', 'EUR', 'KRW']:
            rate.add_field(name=c, value=round(data[c], 3))
        await ctx.send(embed=rate)

    @commands.command()
    async def advice(self, ctx):
        ad = Embed(color=Color.dark_gold())
        ad.title = "Your advice is.."
        base = "https://api.adviceslip.com/advice"
        async with ClientSession() as session:
            data = await get(session, base)
        data = literal_eval(data)
        data = data['slip']
        ad.description = data['advice']
        ad.set_footer(text=f"No: {data['id']}", icon_url="https://i.ibb.co/9g27ggN/advice.png")
        return await ctx.send(embed=ad)

    @commands.command()
    async def chuck(self, ctx):
        ad = Embed(color=Color.dark_gold())
        base = "https://api.chucknorris.io/jokes/random"
        async with ClientSession() as session:
            data = await get(session, base)
        data = literal_eval(data)
        ad.set_author(name="Chuck Norris",
                      icon_url="https://i.ibb.co/swZqcK7/norris.gif",
                      url=data['url'])
        ad.description = data['value']
        return await ctx.send(embed=ad)

    @commands.command(name='comic', aliases=['xkcd'])
    async def comic(self, ctx):
        ad = Embed(color=Color.red())
        base = f"https://xkcd.com/{randrange(1,1001)}/info.0.json"
        async with ClientSession() as session:
            data = await get(session, base)
        data = literal_eval(data)
        ad.set_author(name= data['title'], icon_url="https://i.ibb.co/CtvNjWC/xkcd.png")
        ad.set_image(url=data['img'])
        ad.set_footer(text=f"{data['alt']} ({data['year']})")
        return await ctx.send(embed=ad)

    @commands.command(name='number', aliases=['num'])
    async def number(self, ctx):
        ad = Embed(color=Color.blurple())
        base = "http://numbersapi.com/random/trivia?json"
        async with ClientSession() as session:
            data = await get(session, base)
        data = loads(data)
        if not data['found']:
            return
        ad.set_author(name=data['number'], icon_url="https://i.ibb.co/3cdcpjj/numbers.jpg")
        ad.description = data['text']
        ad.set_footer(text="Powered by Numbers API")
        return await ctx.send(embed=ad)

    @commands.command(name='short', aliases=['url'])
    async def url(self, ctx, url: str):
        ad = Embed(color=Color.gold())
        apiurl = "http://tinyurl.com/api-create.php?url="
        tinyurl = await self.bot.loop.run_in_executor(None, lambda: urlopen(apiurl + url).read().decode("utf-8"))
        ad.title = "URL Shortener 🔁"
        ad.description = tinyurl
        return await ctx.send(embed=ad)
    

def setup(bot):
    bot.add_cog(Rates(bot))