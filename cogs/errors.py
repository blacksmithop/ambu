from discord.ext import commands
from discord import Embed


class Errors(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandNotFound):
            msg = await ctx.send(embed=Embed(
                title=error.args[0]))
            await ctx.message.delete(delay=2)
            await msg.delete(delay=2)

        if isinstance(error, commands.errors.CommandOnCooldown):
            await ctx.send(embed=
                           Embed(title=f"Wait {'%.2f' % error.retry_after}s",
                                 description=f"Cooldown is `{error.cooldown.per}s`"))
        '''
        if isinstance(error, commands.errors.MissingRequiredArgument):
            await ctx.send(embed=Embed(
                title=f"Missing argument {error.param}",
                description=f"```Usage: {self.bot.command_prefix}prefix set new-prefix```"
            ))
        '''

def setup(bot):
    bot.add_cog(Errors(bot))
