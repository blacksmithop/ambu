from discord.ext import commands
from io import StringIO
import sys


class Repl(commands.Cog):
    """Execute Python code.
    """
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.is_owner()
    async def repl(self, ctx, *, code):
        code = code.strip("`").strip(".py")
        old_stdout = sys.stdout
        redirected_output = sys.stdout = StringIO()
        try:
            exec(code)
        except Exception as e:
            print(e)
        sys.stdout = old_stdout
        code = redirected_output.getvalue()
        if code == "":
            code = "Success"
        await ctx.send(f"```py\n{code}```")


def setup(bot):
    bot.add_cog(Repl(bot))
