from discord.ext import commands
from discord import Embed


class Errors(commands.Cog):
    """Error handling.
    """

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        msg = Embed(color=0x0EEA7C)
        if isinstance(error, commands.errors.CommandError):
            msg.title = error.args[0]

        await ctx.send(embed=msg)


def setup(bot):
    bot.add_cog(Errors(bot))
