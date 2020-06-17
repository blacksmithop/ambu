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
        if isinstance(error, commands.errors.CommandNotFound):
            msg.title = "Command not found"
            msg.description = error.args[0]
            return await ctx.send(embed=msg)
        if isinstance(error, commands.errors.MissingRequiredArgument):
            msg.title = "Missing Argument ➖"
            msg.description = error.args[0]
            return await ctx.send(embed=msg)
        if isinstance(error, commands.errors.CommandOnCooldown):
            msg.title = "On Cooldown ⏰"
            msg.description = error.args[0]
            return await ctx.send(embed=msg)
        if isinstance(error, commands.errors.MissingPermissions):
            msg.title = "Missing Permission ⛔"
            msg.description = error.args[0]
            return await ctx.send(embed=msg)
        if isinstance(error, commands.errors.BotMissingAnyRole):
            msg.title = "Bot Missing Role 🤖"
            msg.description = error.args[0]
            return await ctx.send(embed=msg)
        if isinstance(error, commands.errors.NotOwner):
            msg.title = "Owner Only ♾"
            msg.description = error.args[0]
            return await ctx.send(embed=msg)
        if isinstance(error, commands.errors.NSFWChannelRequired):
            msg.title = "NSFW Command 👙"
            msg.description = error.args[0]
            return await ctx.send(embed=msg)
        if isinstance(error, commands.errors.BadArgument):
            msg.title = "Bad Argument 💥"
            msg.description = error.args[0]
            return await ctx.send(embed=msg)
        if isinstance(error, commands.errors.TooManyArguments):
            msg.title = "Extra Arguments ➕"
            msg.description = error.args[0]
            return await ctx.send(embed=msg)
        if isinstance(error, TimeoutError):
            return


def setup(bot):
    bot.add_cog(Errors(bot))
