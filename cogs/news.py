from discord.ext import commands, tasks
from discord import Embed
from discord import Webhook, AsyncWebhookAdapter
from aiohttp import ClientSession
from json import loads


async def get(session: object, url: object) -> object:
    async with session.get(url) as response:
        return await response.text()


class News(commands.Cog):
    """News stream
    """

    def __init__(self, bot):
        self.bot = bot
        self.stream.start()
        self.bot.last_time = "None"

    def cog_unload(self):
        self.stream.cancel()

    @tasks.loop(hours=1.0)
    async def stream(self):
        post = Embed(color=0x9932cc)
        base = "http://newsapi.org/v2/top-headlines?country=in&apiKey=0da077c42ada40f19b0e2d9115170352"
        async with ClientSession() as session:
            data = await get(session, base)
        data = loads(data)
        data = data['articles'][0]
        if self.bot.last_time == data['publishedAt']:
            print("old post")
            return
        post.set_author(name=data['source']['name'], icon_url="https://i.ibb.co/Wg9tLNM/news.png")
        post.set_thumbnail(url=data['urlToImage'])
        post.title = data['title']
        post.url = data['url']
        post.description = data['description']
        self.bot.last_time = data['publishedAt']
        webhook = self.bot.webhook_id
        async with ClientSession() as session:
            webhook = Webhook.from_url(webhook, adapter=AsyncWebhookAdapter(session))
            await webhook.send(embed=post, username='NEWS Feed')

    @stream.before_loop
    async def before_printer(self):
        print('Loading articles...')
        await self.bot.wait_until_ready()


def setup(bot):
    bot.add_cog(News(bot))
