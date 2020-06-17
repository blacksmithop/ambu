from discord.ext import commands
from discord import Embed, Member
from discord.utils import get
import db
from re import sub
from asyncio import sleep


class Admin(commands.Cog):
    """Admin Commands
    """

    def __init__(self, bot):
        self.bot = bot
        self.db = db.BotConfig()
        self.guild = self.bot.get_guild(self.db.fetch(name="emote"))
        self.tick = get(self.guild.emojis, name="agree")

    def pid(self, id: int):
        return int(sub("[<#>]", '', id))

    def rid(self, id: int):
        return int(sub("[<@&>]", '', id))

    @commands.command()
    async def cogs(self, ctx):
        """
        Shows loaded Cogs
        ?cogs
        """
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
        """
        Accept rules and access rest of the Server
        ?accept
        """
        channel = self.db.getchannel(id=ctx.author.guild.id, channel="verify")
        if not channel['channel']:
            return
        cnl = get(ctx.author.guild.channels, id=self.pid(channel['channel']))
        if not cnl == ctx.channel:
            return
        add = self.db.getrole(id=ctx.author.guild.id, role="member")
        if add:
            add = get(ctx.author.guild.roles, id=self.rid(id=add))
            await ctx.message.add_reaction(self.tick)
            await ctx.author.add_roles(add)

    @commands.command()
    @commands.has_permissions(manage_roles=True)
    async def mute(self, ctx, member: Member,
                   num: int):
        """
        Mutes a member
        ?mute member time (in hours)
        """
        if self.bot.user == member or member == ctx.author:
            return
        muted_role = self.db.getrole(id=ctx.author.guild.id, role="muted")
        muted_role = get(ctx.author.guild.roles, id=self.rid(id=muted_role))
        if not muted_role:
            return

        await ctx.send(embed=Embed(
            title=f"Muted {member.display_name} for {num} hours", color=0x2EDF87
        ))
        num = num * 60 * 60

        await ctx.message.add_reaction(self.tick)
        await member.add_roles(muted_role)
        if num > 0:
            await sleep(num)
            for role in member.roles:
                if role == muted_role:
                    await member.remove_roles(muted_role)
                    await ctx.send(embed=Embed(
                        title=f"{member.display_name} is now un-muted", color=0x2EDF87
                    ))
                    break

    @commands.command()
    @commands.has_permissions(manage_roles=True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def unmute(self, ctx, member: Member):
        """
        Unmutes a member
        ?unmute member
        """
        muted_role = self.db.getrole(id=ctx.author.guild.id, role="muted")
        muted_role = get(ctx.author.guild.roles, id=self.rid(id=muted_role))
        if not muted_role:
            return
        if muted_role not in member.roles:
            return
        await ctx.message.add_reaction(self.tick)
        await member.remove_roles(muted_role)
        await ctx.send(embed=Embed(title=f"{member.display_name} was un-muted"))

    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.has_permissions(manage_messages=True)
    async def purge(self, ctx, limit: int = 5, member: Member = None):
        """
        Deleted messages
        ?purge amount
        for purge by user
        ?purge amount member
        """
        if member:
            def is_me(m):
                return m.author == member

            await ctx.channel.purge(limit=limit, check=is_me)
            return
        await ctx.channel.purge(limit=limit + 1)

    @commands.command(name='selfrole', aliases=['sr', 'dis'])
    async def selfrole(self, ctx, role: str = None):
        """
        Get a self role
        ?sr name
        """
        member = ctx.author

        role = get(ctx.guild.roles, name=role)
        s_roles = ['KSD', 'KNR', 'WYD', 'KZK', 'PKD', 'TSR', 'EKM', 'IDK', 'KTM', 'ALP', 'MLP', 'PTA', 'KLM', 'TVM']
        s_roles = [get(ctx.guild.roles, name=r) for r in s_roles]

        r_act = Embed(color=0x4287f5)
        if role is None or role not in s_roles:
            r_act.title = f"Self-roles for {ctx.guild.name}"
            r_act.description = ' '.join([r.name for r in s_roles])
            await ctx.send(embed=r_act)
            return

        mem_roles = [i for i in ctx.author.roles]
        c_role = list(set(s_roles) & set(mem_roles))

        if len(c_role) == 1:
            com = c_role[0].name
            if role.name == com:
                r_act.description = f"⛔ {member.mention}, already has role {role.mention}"
                await ctx.send(embed=r_act)
                return
            else:
                rem_role = get(ctx.guild.roles, name=com)
                await member.remove_roles(rem_role)
                await member.add_roles(role)
                r_act.description = f"⛔ Removed role {rem_role.mention} from {member.mention}\n\n✅ Replaced with {role.mention}"
                await ctx.send(embed=r_act)

        elif len(c_role) == 0:
            await member.add_roles(role)
            r_act.description = f"✅ Added role {role.mention} to {member.mention}"
            await ctx.send(embed=r_act)


def setup(bot):
    bot.add_cog(Admin(bot))
