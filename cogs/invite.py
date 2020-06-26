from discord.ext import commands
from discord import Embed, Color


class Invite(commands.Cog):
    """Invite
    """

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def invite(self, ctx):
        inv = Embed(color=Color.red())
        inv.set_author(name=self.bot.user.name, icon_url=self.bot.user.avatar_url,
                       url="https://blacksmithop.github.io/")
        invite = "[Invite ambu to your server](https://discord.com/oauth2/authorize?client_id=444487257316130827" \
                 "&scope=bot&permissions" \
                 "=1883106513) "
        support = "[Join the support server](https://discord.gg/D8S9yhC)"
        cmds = "[List of commands](https://blacksmithop.github.io/)"
        inv.description = f"{invite}\n{support}\n{cmds}"
        owner = self.bot.get_user(199129403458977792)
        inv.set_footer(text=f"By {owner}", icon_url=owner.avatar_url)
        inv.timestamp = ctx.message.created_at
        await ctx.send(embed=inv)


def setup(bot):
    bot.add_cog(Invite(bot))
