from discord.ext import commands
from discord import Embed, Member
from discord.utils import get
import db
from pickle import loads as l
from re import sub
from asyncio import sleep


class Admin(commands.Cog):
    """Handles the bot's configuration system.
    """

    def __init__(self, bot):
        self.bot = bot
        self.db = db.BotConfig()
        self.guild = self.bot.get_guild(self.db.fetch(name="emote"))
        self.tick = get(self.guild.emojis, name="agree")

    @commands.Cog.listener()
    async def on_member_join(self, member):
        cnl = self.db.getparam(id=member.guild.id, key=["welcome"])
        if not cnl['channel']:
            return
        cnl = {k: l(cnl[k]) for k in cnl.keys()}
        print(cnl)
        id = int(sub("[<#>]", '', cnl['channel']))
        wel = get(member.guild.channels, id=id)
        await wel.send(embed=Embed(
            title=cnl["message"].format(member=member.display_name), color=0x8722EB,
            description=cnl["information"]
        ).set_author(icon_url=member.avatar_url, name=member.display_name))


    @commands.Cog.listener()
    async def on_member_remove(self, member):
        cnl = self.db.getparam(id=member.guild.id, key=["leave"])
        if not cnl['channel']:
            return
        cnl = {k: l(cnl[k]) for k in cnl.keys()}
        id = int(sub("[<#>]", '', cnl['channel']))
        wel = get(member.guild.channels, id=id)
        await wel.send(embed=Embed(
            title=cnl["message"].format(member=member.display_name), color=0x8722EB
        ).set_author(icon_url=member.avatar_url, name=member.display_name))

    @commands.command()
    async def cogs(self, ctx):
        """Shows loaded Cogs"""
        if ctx.invoked_subcommand is None:
            coglist = self.bot.cogs
            cogdir = ""
            for cog in coglist:
                cogdir += f'└──{cog}\n'

            await ctx.send(embed=Embed(
                title="Loaded Cogs ⚙",
                description=f"```{cogdir}```", color=0xEA0E0E
            ))

    @commands.command()
    @commands.has_role("Joined")
    async def accept(self, ctx):
        cnl = self.db.getparam(id=ctx.author.guild.id, key=["verification"])
        if not cnl["verify"]:
            return
        cnl = {k: l(cnl[k]) for k in cnl.keys()}
        id = int(sub("[<#>]", '', cnl['verify']))
        if not get(ctx.author.guild.channels, id=id) == ctx.channel:
            return
        remove = cnl["joinrole"]
        add = self.db.getparam(id=ctx.author.guild.id, key=["roles", "member"])
        if add and remove:
            add = int(sub('[<@&>]', '', add))
            remove = int(sub('[<@&>]', '', remove))
            add = get(ctx.guild.roles, id=add)
            remove = get(ctx.guild.roles, id=remove)
            await ctx.message.add_reaction(self.tick)
            await ctx.author.add_roles(add)
            await ctx.author.remove_roles(remove)

    @commands.command()
    @commands.has_permissions(manage_roles=True)
    async def mute(self, ctx, member: Member,
                   num: int, unit: str):
        """Mutes a member"""
        if self.bot.user == member or member == ctx.author:
            return
        m = self.db.getparam(id=ctx.guild.id, key=["roles", "muted"])
        if not m:
            return
        id = int(sub('[<@&>]', '', m))
        muted_role = get(ctx.guild.roles, id=id)

        if unit in ['s', 'sec', 'second', 'seconds']:
            num = num
        if unit in ['m', 'min', 'minute', 'minutes']:
            num = num * 60
        if unit in ['h', 'hr', 'hour', 'hours']:
            num = num * 60 * 60
        await ctx.message.add_reaction(self.tick)
        await member.add_roles(muted_role)

        await ctx.send(embed=Embed(
            title=f"Muted {member.display_name} for {num}{unit}", color=0x2EDF87
        ))

        if num > 0:
            await sleep(num)
            for role in member.roles:
                if role.name == "Muted":
                    await member.remove_roles(muted_role)
                    await ctx.send(embed=Embed(
                        title=f"{member.display_name} is now un-muted", color=0x2EDF87
                    ))

    @commands.command()
    @commands.has_permissions(manage_roles=True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def unmute(self, ctx, member: Member):
        """Unmutes a member"""
        m = self.db.getparam(id=ctx.guild.id, key=["roles", "muted"])
        if not m:
            return
        id = int(sub('[<@&>]', '', m))
        muted_role = get(ctx.guild.roles, id=id)
        if muted_role not in member.roles:
            return
        await ctx.message.add_reaction(self.tick)
        await member.remove_roles(muted_role)
        await ctx.send(embed=Embed(title=f"{member.display_name} was un-muted"))

    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.has_permissions(manage_messages=True)
    async def purge(self, ctx, limit: int = 5, member: Member = None):
        """Deleted messages"""
        if member:
            def is_me(m):
                return m.author == member

            await ctx.channel.purge(limit=limit, check=is_me)
            return
        await ctx.channel.purge(limit=limit + 1)


def setup(bot):
    bot.add_cog(Admin(bot))