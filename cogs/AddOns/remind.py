from os import getenv as e
from discord.ext import commands, tasks
from discord import Webhook, AsyncWebhookAdapter
from aiohttp import ClientSession


class Remind(commands.Cog):
    """Error handling.
    """

    def __init__(self, bot):
        self.index = 0
        self.bot = bot
        self.bump.start()

    def cog_unload(self):
        self.bump.cancel()

    @tasks.loop(hours=2.0)
    async def bump(self):
        async with ClientSession() as session:
            webhook = Webhook.from_url(e('wh_token'), adapter=AsyncWebhookAdapter(session))
            await webhook.send('<@&685199045114855432> Time to bump!', username='Bump')

    @bump.before_loop
    async def before_printer(self):
        print('waiting...')
        await self.bot.wait_until_ready()


def setup(bot):
    bot.add_cog(Remind(bot))
