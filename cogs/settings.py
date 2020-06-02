from discord.ext import commands
from discord import Embed, Role, TextChannel
from typing import Union
import sys
import os.path

sys.path.append(os.path.join(os.path.dirname(__file__), 'ambu/'))
from db import BotConfig

class Settings(commands.Cog):
    """Bot Settings.
    """

    def __init__(self, bot):
        self.bot = bot
        self.db = BotConfig()

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        self.db.add(id=guild.id)

    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        self.db.remove(id=guild.id)

    @commands.command()
    async def info(self, ctx):
        guild = ctx.guild
        stats = self.db.get(id=guild.id)
        info = Embed(title=f"Settings for {guild.name}", color=0xF58413)
        info.set_author(icon_url=self.bot.user.avatar_url, name=self.bot.user.display_name, url="https://github.com/blacksmithop/ambu")
        for k in stats.keys():
            info.add_field(name=k, value=stats[k], inline=True)
        info.set_footer(text="⚙", icon_url=ctx.author.avatar_url)
        info.timestamp = ctx.message.created_at
        await ctx.send(embed=info)

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def set(self, ctx, key: str, value: Union[TextChannel, Role, str, bool] = None):

        if not key in self.db.guild_stats.keys():
            return
        stats = Embed(color=0xF58413)
        stats.timestamp = ctx.message.created_at
        stats.set_author(icon_url=self.bot.user.avatar_url, name=self.bot.user.display_name, url="https://github.com/blacksmithop/ambu")
        if value is None:
            stats.title = key
            val = self.db.get(id=ctx.guild.id, key=key)
            stats.description = val or "None"
        else:
            if key in ["welcome", "leave", "verify", "testing", "logs"]:
                if value not in ctx.guild.text_channels:
                    return
                value = value.mention
            if key in ["member", "muted"]:
                if value not in ctx.guild.roles:
                    return
                value = value.mention
            if key == "prefix" and value == self.bot.command_prefix:

                return
            if self.db.set(id=ctx.guild.id, key=key, value=value):
                stats.description = f"Set {key} to {value}"
        stats.set_footer(text="🔄", icon_url=ctx.author.avatar_url)
        await ctx.send(embed=stats)


def setup(bot):
    bot.add_cog(Settings(bot))
