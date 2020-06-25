from discord.ext import commands
from datetime import datetime
from discord import Embed, __version__
import platform, psutil
from os import getpid


class Info(commands.Cog):
    """Bot Statistics
    """

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='uptime', aliases=['up'])
    async def uptime(self, ctx):
        """
        Get stats about the bot
        ?uptime
        """
        up = Embed(color=0xf59042)
        up.set_author(name=self.bot.user.display_name,
                      icon_url=self.bot.user.avatar_url,
                      url="https://blacksmithop.github.io/")

        now = datetime.utcnow()
        delta = now - self.bot.uptime
        h, remainder = divmod(int(delta.total_seconds()), 3600)
        m, s = divmod(remainder, 60)
        d, h = divmod(h, 24)

        if d:
            time_up = f"**{d}** days, **{h}** hours, **{m}** minutes, and **{s}** seconds."
        else:
            time_up = f"**{h}** hours, **{m}** minutes, and **{s}** seconds."

        up.add_field(name="Uptime", value=time_up, inline=True)
        up.add_field(name="Platform", value=platform.system(), inline=True)
        up.add_field(name="Architecture", value=platform.machine(), inline=True)
        up.add_field(name="RAM",
                     value=str(round(psutil.virtual_memory().total / (1024.0 ** 3))) + " GB",
                     inline=True)
        up.add_field(name="discord.py", value=__version__, inline=True)
        process = psutil.Process(getpid())
        usage = process.memory_info().rss
        usage = usage/1e+6
        up.add_field(name="Usage", value=f"{round(usage,3)} MB", inline=True)
        await ctx.send(embed=up)


def setup(bot):
    bot.add_cog(Info(bot))
