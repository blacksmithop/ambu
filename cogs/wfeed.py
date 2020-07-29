from discord.ext import commands, tasks
from discord import Embed
from discord import Webhook, AsyncWebhookAdapter
from aiohttp import ClientSession
from json import loads


async def get(session: object, url: object) -> object:
    async with session.get(url) as response:
        return await response.text()


class Feed(commands.Cog):
    """Reddit feed
    """

    def __init__(self, bot):
        self.bot = bot
        self.world.start()
        self.bot.prev_news = "Default"

    def cog_unload(self):
        self.world.cancel()

    @tasks.loop(hours=2.0)
    async def world(self):
        post = Embed(color=0xFF5700)
        base = "https://www.reddit.com/r/worldnews/new.json?sort=new&limit=1"
        async with ClientSession() as session:
            data = await get(session, base)
        data = loads(data)
        data = data['data']['children'][0]['data']
        if data['author_fullname'] == self.bot.prev_news:
            print("same post")
            return
        post.set_author(icon_url="https://i.ibb.co/vxFJ9dr/news.png",
                        name="r/WorldNews", url="https://www.reddit.com/r/worldnews/")
        post.title = data['title']
        post.url = f"https://www.reddit.com{data['permalink']}"
        if data['thumbnail'] not in ['default', 'self']:
            post.set_thumbnail(url=data['thumbnail'])
        post.add_field(name="Comments 📜", value=data['num_comments'])
        post.add_field(name="Score 💹", value=data['score'])
        self.bot.prev_news = data['author_fullname']
        webhook = self.bot.webhook_id
        async with ClientSession() as session:
            webhook = Webhook.from_url(webhook, adapter=AsyncWebhookAdapter(session))
            await webhook.send(embed=post, username='r/Worldnews Feed')

    @world.before_loop
    async def before_printer(self):
        print('World News Feed...')
        await self.bot.wait_until_ready()


def setup(bot):
    bot.add_cog(Feed(bot))
