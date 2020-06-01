from aiohttp import web
import asyncio
from discord.ext import commands


class Server(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.port = 9090

    async def webserver(self):
        async def handler(request):
            return web.Response(text=f"Running {self.bot.user.display_name} Bot")

        app = web.Application()
        app.router.add_get('/', handler)

        runner = web.AppRunner(app)
        await runner.setup()
        self.site = web.TCPSite(runner, '0.0.0.0', self.port)
        await self.bot.wait_until_ready()
        print(f"Running Webserver at: Port {self.port}")
        await self.site.start()

    def __unload(self):
        asyncio.ensure_future(self.site.stop())


def setup(bot):
    yt = Server(bot)
    bot.add_cog(yt)
    bot.loop.create_task(yt.webserver())
