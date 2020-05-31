from discord.ext import commands
from discord import Embed


class Help(commands.Cog):
    """Help command.
    """

    def __init__(self, bot):
        self.bot = bot
        bot.remove_command("help")

    @commands.command()
    async def help(self, ctx):
        cogs = {"🛠 Config": "Configure the bot", "🧾 Log": "Setup logging", "📷 Image": "Image commands"}
        hembed = Embed()
        hembed.title = f"Cogs"
        hembed.set_author(name=self.bot.user.display_name,
                          url="https://github.com/blacksmithop/ambu",
                          icon_url=self.bot.user.avatar_url)
        for cog in cogs.keys():
            hembed.add_field(name=cog, value=f"`{cogs[cog]}`", inline=True)
        hembed.set_footer(text=f"Do {self.bot.command_prefix}help [category] for more",
                          icon_url=ctx.author.avatar_url)
        await ctx.send(embed=hembed)


def setup(bot):
    bot.add_cog(Help(bot))
