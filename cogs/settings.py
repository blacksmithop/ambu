from discord.ext import commands
from ambu import db
from discord import Embed
from pickle import loads as l, dumps as d


class Settings(commands.Cog):
    """Bot Settings.
    """

    def __init__(self, bot):
        self.bot = bot
        self.db = db.BotConfig()

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        self.db.addguild(id=guild.id)

    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        self.db.removeguild(id=guild.id)

    @commands.command()
    async def info(self, ctx):
        guild = ctx.guild
        stats = self.db.getguild(id=guild.id)
        info = Embed(title=f"Settings for {guild.name}", color=0xF58413)
        info.set_author(icon_url=self.bot.user.avatar_url, name=self.bot.user.display_name,
                        url="https://github.com/blacksmithop/ambu")
        for k in stats.keys():
            v = stats[k]
            if type(v) == dict:
                value = ""
                for i in v:
                    value += f"`{i}`: {l(v[i])}\n"
                info.add_field(name=k, value=value, inline=True)
            elif type(v) is bytes:
                info.add_field(name=k, value=l(v), inline=True)
        info.set_footer(text="⚙", icon_url=ctx.author.avatar_url)
        info.timestamp = ctx.message.created_at
        await ctx.send(embed=info)

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def set(self, ctx, k1, k2, *, value=None):
        act = Embed()
        if not self.db.r.exists(ctx.guild.id):
            return
        if k1 in self.db.guild.keys():
            if k2 and value is None:
                if type(self.db.guild[k1]) is dict:
                    if k2 in self.db.guild[k1].keys():
                        self.db.setparam(id=ctx.guild.id, key=[k1], value=d(k2))
                        act.description = f"Set `{k1}` to {k2}"
                else:
                    self.db.setparam(id=ctx.guild.id, key=[k1], value=d(k2))
                    act.description = f"Set `{k1}` to {k2}"
            else:
                self.db.setparam(id=ctx.guild.id, key=[k1, k2], value=d(value))
                act.description = f"Set `{k1}` `{k2}` to {value}"
        await ctx.send(embed=act)


def setup(bot):
    bot.add_cog(Settings(bot))
