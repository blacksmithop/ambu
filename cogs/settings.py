from discord.ext import commands
import db
from discord import Embed
from asyncio import TimeoutError


class Settings(commands.Cog):
    """Bot Configuration
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
    async def info(self, ctx, p: int = 1):
        """
        Shows current server-settings for the bot
        """
        guild = ctx.guild
        stats = self.db.getguild(id=guild.id)
        info = Embed(title=f"Settings for {guild.name}", color=0xF58413)
        info.set_author(icon_url=self.bot.user.avatar_url, name=self.bot.user.display_name,
                        url="https://github.com/blacksmithop/ambu")

        one = ['welcome', 'logs', 'leave']
        two = ['roles', 'filter', 'testing']
        t = ['◀', '⏸', '▶']

        def p2e(page: int):
            info = Embed(color=0xd42300)
            if page == 0:
                w = self.db.getchannel(id=guild.id, channel='welcome')
                info.title = "Welcome"
                for k in w:
                    info.add_field(name=k, value=w[k])

            if page == 1:
                w = self.db.getchannel(id=guild.id, channel='logs')
                info.title = "Logs"
                for k in w:
                    info.add_field(name=k, value=w[k])

            if page == 2:
                w = self.db.getchannel(id=guild.id, channel='leave')
                t = self.db.getchannel(id=guild.id, channel='testing')
                info.title = "Leave"
                for k in w:
                    info.add_field(name=k, value=w[k])
                for k in t:
                    info.add_field(name="testing", value=t[k])

            if page == 3:
                r = self.db.getrole(id=guild.id)
                info.title = "Roles"
                for k in r:
                    info.add_field(name=k, value=r[k])

            if page == 4:
                r = self.db.getfilter(id=guild.id)
                info.title = "Filters"
                for k in r:
                    info.add_field(name=k, value=r[k])
            info.set_footer(text=f"Page {page + 1}/5")
            return info

        msg = await ctx.send(embed=p2e(page=p - 1))
        for e in t:
            await msg.add_reaction(e)

        def reac_check(r, u):
            return msg.id == r.message.id and u != self.bot.user and r.emoji in t

        page = 0
        while True:
            try:
                reaction, user = await self.bot.wait_for('reaction_add', timeout=20.0, check=reac_check)
                em = str(reaction.emoji)
                if user != self.bot.user:
                    await msg.remove_reaction(emoji=em, member=user)
            except TimeoutError:
                await msg.edit(embed=Embed(description="```Exited ⛔```"))
                break
            if em == t[0]:
                if page == 0:
                    return
                else:
                    page -= 1
                    await msg.edit(embed=p2e(page=page))
            if em == t[2]:
                if page == 4:
                    return
                else:
                    page += 1
                    await msg.edit(embed=p2e(page=page))
            if em == t[1]:
                return

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def filter(self, ctx, key: str, value: str):
        """
        Sets the filters for the bot
        ?set filter True/False
        """
        if key and value in ['True', 'False']:
            if self.db.setfilter(id=ctx.guild.id, key=key, value=value):
                await ctx.send(embed=Embed(description=f"Set `{key}` filter to `{value}`"))

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def channel(self, ctx, key: str, v1: str, *, v2: str = None):
        """
        Configures channel settings (check the detailed help)
        ?channel name setting result
        """
        if not v2:
            v2 = v1
            v1 = "channel"
        if '&' in v2:
            return
        if key and v1 and v2:
            if self.db.setchannel(id=ctx.guild.id, key=key, v1=v1, v2=v2):
                await ctx.send(embed=Embed(description=f"Set `{key}` `{v1}` to {v2}"))

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def role(self, ctx, key: str, *, value: str):
        """
        Configures Role settings (check the detailed help)
        ?role type name
        """
        if key and value:
            if '&' not in value:
                return
            if self.db.setrole(id=ctx.guild.id, key=key, value=value):
                await ctx.send(embed=Embed(description=f"Set `{key}` role to {value}"))

    @commands.command()
    async def prefix(self, ctx, new_prefix: str = None):
        if not new_prefix:
            return await ctx.send(embed=Embed(title=f"Prefix for {ctx.guild.name}",
                                              description=self.db.getprefix(id=ctx.guild.id) or '?'))
        if self.db.setprefix(id=ctx.guild.id, new_prefix=new_prefix):
            return await ctx.send(embed=Embed(title=f"Prefix for {ctx.guild.name}",
                                              description=f"Set to {self.db.getprefix(id=ctx.guild.id)}"))


def setup(bot):
    bot.add_cog(Settings(bot))
