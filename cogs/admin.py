from discord.ext import commands
from discord import Embed, Member
from discord.utils import get
from os import listdir as l
from asyncio import sleep
from ambu.db import BotConfig


class Admin(commands.Cog):
    """Handles the bot's configuration system.
    """

    def __init__(self, bot):
        self.bot = bot
        self.db = BotConfig()
        self.guild = self.bot.get_guild(int(self.db.value(key="emotes")))
        self.tick = get(self.guild.emojis, name="tick")

    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def prefix(self, ctx):
        """Shows the bot Prefix
        """
        if ctx.invoked_subcommand is None:
            p = self.db.get(id=ctx.guild.id, key="prefix") or self.bot.command_prefix
            await ctx.send(embed=Embed(title=f"Prefix for {ctx.guild.name}",
                                       description=f"```{p}```",
                                       color=0x40D7D7))

    @commands.Cog.listener()
    async def on_member_join(self, member):
        channel = get(member.guild.channels, name="welcome")
        await channel.send(embed=Embed(
            title=f"Welcome to the server!", color=0x8722EB
        ).set_author(icon_url=member.avatar_url, name=member.display_name))
        role = get(member.guild.roles, name="Joined")
        await member.add_roles(role)

    @commands.group()
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

    @cogs.group()
    async def all(self, ctx):
        """Shows available Cogs"""
        cogdir = ""
        for cog in l("cogs"):
            if ".py" in cog:
                cog = cog.replace(".py", "")
                cogdir += f'└──{cog}\n'

        await ctx.send(embed=Embed(
                title="Cogs ⚙",
                description=f"```{cogdir}```", color=0xEA0E0E
            ))
    @commands.group()
    @commands.has_permissions(administrator=True)
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def setchannel(self, ctx):
        """Configures Channels"""
        if ctx.invoked_subcommand is None:

            base_role = get(ctx.guild.roles, name="Member")
            yet_to_verify = get(ctx.guild.roles, name="Joined")
            muted = get(ctx.guild.roles, name="Muted")
            dev_role = get(ctx.guild.roles, name="Dev")

            tchannels = ctx.guild.text_channels
            vchannels = ctx.guild.voice_channels
            tchannels = [i for i in tchannels if i.name not in ["welcome", "rules", "logs", "testing"]]

            for channel in tchannels:
                await channel.set_permissions(base_role,
                                              add_reactions=True, send_messages=True, read_messages=True,
                                              read_message_history=True,
                                              change_nickname=True, manage_emojis=True, embed_links=True,
                                              attach_files=True)

                await channel.set_permissions(ctx.guild.default_role, send_messages=False, read_messages=False,
                                              read_message_history=False)

                await channel.set_permissions(muted, send_messages=False, read_messages=False,
                                              read_message_history=False)

            for channel in vchannels:
                await channel.set_permissions(base_role, connect=True, speak=True, stream=True)

            welcome = get(ctx.guild.text_channels, name="welcome")
            await welcome.set_permissions(base_role, read_messages=True, send_messages=False, read_message_history=True)
            await welcome.set_permissions(ctx.guild.default_role, send_messages=False, read_messages=True,
                                          read_message_history=False)

            rules = get(ctx.guild.text_channels, name="rules")

            await rules.set_permissions(yet_to_verify, send_messages=True, add_reactions=False, read_messages=True,
                                        read_message_history=True)
            await rules.set_permissions(ctx.guild.default_role, send_messages=False, read_messages=False,
                                        read_message_history=False)

            logs = get(ctx.guild.text_channels, name="logs")
            await logs.set_permissions(ctx.guild.default_role, send_messages=False, read_messages=False,
                                       read_message_history=False)
            await logs.set_permissions(muted, send_messages=False, read_messages=False,
                                       read_message_history=False)
            await logs.set_permissions(base_role, send_messages=False, read_messages=True,
                                       read_message_history=True, add_reactions=False)

            testing = get(ctx.guild.channels, name="testing")
            await testing.set_permissions(ctx.guild.default_role, read_messages=False)
            await testing.set_permissions(dev_role, read_messages=True, embed_links=True)
            await ctx.message.add_reaction(self.tick)
            await rules.send(content="Send ?accept to access rest of the server")
            for member in ctx.guild.members:
                if not member.bot:
                    await member.add_roles(base_role)

            await ctx.send(embed=Embed(
                title="Success",
                description=""" Set Member as default role\n Joined as unverified role
                \n Muted as muted role\n Dev as testing role"""
            ))

    @setchannel.group()
    async def role(self, ctx):
        """Configures Roles"""
        if get(ctx.guild.roles, name="Member") is None:
            await ctx.guild.create_role(name="Member")
        if get(ctx.guild.roles, name="Joined") is None:
            await ctx.guild.create_role(name="Joined")
        if get(ctx.guild.roles, name="Muted") is None:
            await ctx.guild.create_role(name="Muted")
        if get(ctx.guild.roles, name="Dev") is None:
            await ctx.guild.create_role(name="Dev")
        await ctx.message.add_reaction(self.tick)
        await ctx.send(embed=Embed(
            description="Created roles Member, Joined, Muted, Dev"
        ))

    @commands.command()
    @commands.has_role("Joined")
    async def accept(self, ctx):
        """Accepts and gets Member tag"""
        if ctx.channel.name == "rules":
            await ctx.message.add_reaction(self.tick)
            add = get(ctx.guild.roles, name="Member")
            await ctx.author.add_roles(add)
            remove = get(ctx.guild.roles, name="Joined")
            await ctx.author.remove_roles(remove)

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.channel.name == "rules" and message.author != self.bot.user:
            await message.delete(delay=2)

    @commands.command()
    @commands.has_permissions(manage_roles=True)
    async def mute(self, ctx, member: Member,
                   num: int, unit: str):
        """Mutes a member"""
        if self.bot.user == member or member == ctx.author:
            await ctx.send("Self-mute is disabled")
            return
        muted_role = get(ctx.guild.roles, name="Muted")

        if unit in ['s', 'sec', 'second', 'seconds']:
            num = num
        if unit in ['m', 'min', 'minute', 'minutes']:
            num = num * 60
        if unit in ['h', 'hr', 'hour', 'hours']:
            num = num * 60 * 60
        await ctx.message.add_reaction(self.tick)
        await member.add_roles(muted_role)

        await ctx.send(embed=Embed(
            title=f"Muted {member.display_name}"
        ))

        if num > 0:
            await sleep(num)
            await member.remove_roles(muted_role)
            for role in member.roles:
                if role.name == "Muted":
                    await ctx.send(embed=Embed(
                        title=f"Unmuted {member.display_name}"
                    ))

    @commands.command()
    @commands.has_permissions(manage_roles=True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def unmute(self, ctx, member: Member):
        """Unmutes a member"""
        muted = None
        for role in member.roles:
            if role.name == "Muted":
                muted = role
        if muted is not None:
            await ctx.message.add_reaction(self.tick)
            await member.remove_roles(muted)
            await ctx.send(embed=Embed(
                title=f"Unmuted {member.display_name}"
            ))

    @commands.command()
    @commands.is_owner()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def disable(self, ctx, cmd):
        """Disables a Command"""
        for x in self.bot.get_command(cmd).commands:
            x.enabled = False
        await ctx.message.add_reaction(self.tick)
        self.bot.get_command(cmd).update()

    @commands.group(invoke_without_command=True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.has_permissions(manage_messages=True)
    async def purge(self, ctx, limit: int = 1):
        """Deleted messages"""
        if ctx.invoked_subcommand is None:
            await ctx.channel.purge(limit=limit + 1)

    @purge.group(invoke_without_command=True)
    async def by(self, ctx, member: Member, limit: int = 10):
        """Deleted messages by user"""

        def is_me(m):
            return m.author == member

        await ctx.channel.purge(limit=limit, check=is_me)


def setup(bot):
    bot.add_cog(Admin(bot))
