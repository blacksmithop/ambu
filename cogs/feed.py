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
        self.reddit.start()
        self.bot.prev_post = "Default"

    def cog_unload(self):
        self.reddit.cancel()

    @tasks.loop(hours=1.0)
    async def reddit(self):
        print(0, self.bot.prev_post)
        post = Embed(color=0xFF5700)
        base = "https://www.reddit.com/r/kerala/new.json?sort=new&limit=1"
        async with ClientSession() as session:
            data = await get(session, base)
        data = loads(data)
        data = data['data']['children'][0]['data']
        if data['author_fullname'] == self.bot.prev_post:
            print(1, self.bot.prev_post)
            print("same post")
            return
        post.set_author(icon_url="https://i.ibb.co/4FLWrf5/community-Icon-sb8lb3clguv01.png",
                        name="r/Kerala", url="https://www.reddit.com/r/Kerala/")
        post.title = data['title']
        post.url = f"https://www.reddit.com{data['permalink']}"
        if data['thumbnail'] not in ['default', 'self']:
            post.set_thumbnail(url=data['thumbnail'])
        post.add_field(name="Comments 📜", value=data['num_comments'])
        post.add_field(name="Score 💹", value=data['score'])
        self.bot.prev_post = data['author_fullname']
        print(2, self.bot.prev_post)
        webhook = "https://ptb.discordapp.com/api/webhooks/727170137458868295/iBlEkK0oxegk4teNZeynNBsBTzH-WtHSNCSYmLHvGL7HE5T_fIfZjmUSnBzivIkPNlMo"
        async with ClientSession() as session:
            webhook = Webhook.from_url(webhook, adapter=AsyncWebhookAdapter(session))
            await webhook.send(embed=post, username='r/Kerala Feed')

    @reddit.before_loop
    async def before_printer(self):
        print('Loading feed...')
        await self.bot.wait_until_ready()


def setup(bot):
    bot.add_cog(Feed(bot))
