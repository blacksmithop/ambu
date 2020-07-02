from discord.ext import commands, tasks
from discord import Embed, Color
from aiohttp import ClientSession
from json import loads
from discord import Webhook, AsyncWebhookAdapter


async def get(session: object, url: object) -> object:
    async with session.get(url) as response:
        return await response.text()


class NYTimes(commands.Cog):
    """NYTimes
    """

    def __init__(self, bot):
        self.bot = bot
        self.nytfeed.start()
        self.bot.nyfeed = "None"

    @commands.command()
    async def book(self, ctx, *, name):
        name = name.title()
        name = '+'.join(name.split())
        detail = Embed(color=Color.magenta())
        base = f"https://api.nytimes.com/svc/books/v3/reviews.json?title={name}&api-key=zxkRPqZijNjfIAmybtASgi8GgChlYHE4"
        async with ClientSession() as session:
            data = await get(session, base)
        data = loads(data)
        if data['num_results'] == 0:
            return
        data = data['results'][0]
        detail.title = data['book_title']
        detail.url = data['url']
        detail.description = f"By {data['book_author']}"
        if data['summary'] != "":
            detail.add_field(name="Summary", value=data['summary'])
        detail.set_footer(text=f"Published at {data['publication_dt']}")
        return await ctx.send(embed=detail)

    @commands.command()
    async def author(self, ctx, *, name):
        name = name.title()
        name = '+'.join(name.split())
        detail = Embed(color=Color.magenta())
        base = f"https://api.nytimes.com/svc/books/v3/reviews.json?author={name}&api-key=zxkRPqZijNjfIAmybtASgi8GgChlYHE4"
        async with ClientSession() as session:
            data = await get(session, base)
        data = loads(data)
        if data['num_results'] == 0:
            return
        data = data['results']
        detail.title = f"Works by {data[0]['book_author']}"
        if len(data) >=3:
            j = 3
        if len(data) == 2:
            j = 2
        else:
            j == 1
        for i in range(1, j+1):
            fact = ""
            fact += f"Title: {data[i-1]['book_title']}\n"
            fact += f"Published: {data[i - 1]['publication_dt']}\n"
            if data[i - 1]['summary'] != "":
                fact += f"Summary: {data[i - 1]['summary']}\n"
            detail.add_field(name=str(i), value=f"```{fact}```")
        return await ctx.send(embed=detail)

    def cog_unload(self):
        self.nytfeed.cancel()

    @tasks.loop(hours=1.0)
    async def nytfeed(self):
        post = Embed(color=Color.green())
        base = "https://api.nytimes.com/svc/news/v3/content/all/all.json?api-key=zxkRPqZijNjfIAmybtASgi8GgChlYHE4"
        async with ClientSession() as session:
            data = await get(session, base)
        data = loads(data)['results'][0]
        if data['title'] == self.bot.nyfeed:
            print('same post')
            return
        post.title = data['title']
        post.url = data['url']
        post.description = data['abstract']
        post.set_author(name=data['source'], icon_url="https://i.ibb.co/Qksb3Nx/nyt.png")
        if data['multimedia']:
            post.set_thumbnail(url=data['multimedia'][0]['url'])
        webhook = "https://ptb.discordapp.com/api/webhooks/727170137458868295/iBlEkK0oxegk4teNZeynNBsBTzH-WtHSNCSYmLHvGL7HE5T_fIfZjmUSnBzivIkPNlMo"
        async with ClientSession() as session:
            webhook = Webhook.from_url(webhook, adapter=AsyncWebhookAdapter(session))
            await webhook.send(embed=post, username='NY Times Feed')

    @nytfeed.before_loop
    async def before_printer(self):
        print('Loading feed...')
        await self.bot.wait_until_ready()

def setup(bot):
    bot.add_cog(NYTimes(bot))
