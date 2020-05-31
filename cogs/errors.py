from discord.ext import commands
from discord import Embed


class Errors(commands.Cog):
    """Error handling.
    """
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandNotFound):
            await ctx.send(embed=Embed(
                title=error.args[0]), delete_after=3)
            await ctx.message.delete(delay=2)

        if isinstance(error, commands.errors.CommandOnCooldown):
            await ctx.send(embed=
                           Embed(title=f"Wait {'%.2f' % error.retry_after}s",
                                 description=f"Cooldown is `{error.cooldown.per}s`"))

        if isinstance(error, commands.errors.MissingRequiredArgument):
            await ctx.send(embed=Embed(
                title=f"Missing argument",
                description=f"```{error}```"
            ))


def setup(bot):
    bot.add_cog(Errors(bot))
