from discord.ext import commands
from discord import Embed, Member
from discord.utils import get
from os import listdir as l
from asyncio import sleep
from discord import Status, Game

class Config(commands.Cog):
    """Handles the bot's configuration system.
    """

    def __init__(self, bot):
        self.bot = bot

    @commands.group()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def prefix(self, ctx):
        """Shows the bot Prefix
        """
        if ctx.invoked_subcommand is None:
            pfx = [i for i in self.bot.command_prefix if '<' not in i]
            await ctx.send(embed=Embed(
                title="Prefixes",
                description=pfx[0]))

    @prefix.group(invoke_without_command=True)
    @commands.has_permissions(administrator=True)
    async def set(self, ctx, new_prefix):
        """Sets the bot Prefix, adds playing status"""
        self.bot.command_prefix = new_prefix
        await ctx.send(embed=Embed(
            title="Prefix Set",
            description=f"Changed Prefix to {new_prefix}"
        ))
        self.bot.unload_extension("cogs.errors")
        self.bot.load_extension("cogs.errors")
        await self.bot.change_presence(status=Status.online, activity=Game(name=f"{self.bot.command_prefix}help"))

    @prefix.group()
    @commands.has_permissions(administrator=True)
    async def mention(self, ctx):
        """Sets the Prefix to Mention"""
        self.bot.command_prefix = [f'<@!{self.bot.user.id}> ', f'<@{self.bot.user.id}> ', self.bot.command_prefix, ]
        await ctx.send(f"<@{self.bot.user.id}>")

    @commands.Cog.listener()
    async def on_member_join(self, member):
        channel = get(member.guild.channels, name="welcome")
        await channel.send(embed=Embed(
            title=f"{member.display_name} has joined the server"
        ))
        role = get(member.guild.roles, name="Joined")
        await member.add_roles(role)

    @commands.group()
    @commands.is_owner()
    async def cogs(self, ctx):
        """Shows available Cogs"""
        if ctx.invoked_subcommand is None:
            cogdir = ""
            for cog in l("cogs"):
                if ".py" in cog:
                    cog = cog.replace(".py", "")
                    cogdir += f'└──{cog}\n'

            await ctx.send(embed=Embed(
                title="Cogs ⚙",
                description=f"```{cogdir}```"
            ))

    @cogs.group()
    async def show(self, ctx):
        """Shows loaded Cogs"""
        coglist = self.bot.cogs
        cogdir = ""
        for cog in coglist:
            cogdir += f'└──{cog}\n'

        await ctx.send(embed=Embed(
            title="Loaded Cogs ⚙",
            description=f"```{cogdir}```"
        ))

    @cogs.group()
    async def unload(self, ctx, cog):
        """Unloads a Cog"""
        coglist = [i.lower() for i in self.bot.cogs]
        if cog in coglist:
            self.bot.unload_extension(f"cogs.{cog}")
            await ctx.send(embed=Embed(
                title=f"Unloaded Cog: {cog}"
            ))

    @cogs.group()
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def reload(self, ctx, cog):
        """Reloads a Cog"""
        coglist = [i.lower() for i in self.bot.cogs]
        if cog in coglist:
            self.bot.unload_extension(f"cogs.{cog}")
            self.bot.load_extension(f"cogs.{cog}")
            await ctx.send(embed=Embed(
                title=f"Reloaded Cog: {cog}"
            ))

    @cogs.group()
    async def load(self, ctx, cogout):
        """Loads a Cog"""
        for cog in l("cogs"):
            if ".py" in cog:
                cogin = cog.replace(".py", "")
                if cogin == cogout:
                    self.bot.load_extension(f"cogs.{cogin}")
                    await ctx.send(embed=Embed(
                        title=f"Loaded Cog: {cogin}"
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
            tchannels = ctx.guild.text_channels
            vchannels = ctx.guild.voice_channels
            tchannels = [i for i in tchannels if i.name not in ["welcome", "rules", "logs"]]

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
            await rules.send(content="Send ?accept to access rest of the server")
            for member in ctx.guild.members:
                if not member.bot:
                    await member.add_roles(base_role)

            await ctx.send(embed=Embed(
                title="Success",
                description="Set Member as default role\n Set Joined as unverified role\n Muted as muted role"
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
        await ctx.send(embed=Embed(
            description="Created roles Member, Joined, Muted"
        ))

    @commands.command()
    @commands.has_role("Joined")
    async def accept(self, ctx):
        """Accepts and gets Member tag"""
        if ctx.channel.name == "rules":
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
        self.bot.get_command(cmd).update()

    @commands.group(invoke_without_command=True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.has_permissions(manage_messages=True)
    async def purge(self, ctx, limit: int = 1):
        """Deleted messages"""
        if ctx.invoked_subcommand is None:
            await ctx.channel.purge(limit=limit + 1)
            await ctx.trigger_typing()
            done = await ctx.send(f"Cleaning {limit} messages")
            await done.delete(delay=2)

    @purge.group(invoke_without_command=True)
    async def by(self, ctx, member: Member, limit: int = 10):
        """Deleted messages by user"""
        def is_me(m):
            return m.author == member

        await ctx.channel.purge(limit=limit, check=is_me)
        done = await ctx.send(f"Cleaned {limit} messages by {member.display_name}")
        await done.delete(delay=2)


def setup(bot):
    bot.add_cog(Config(bot))
