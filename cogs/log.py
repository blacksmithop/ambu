from discord.ext import commands
from discord import Embed, Member, Colour, Role, Status, Guild
from discord.utils import get
from datetime import datetime as dt


class Log(commands.Cog):
    """Logging system.
    """

    def __init__(self, bot):
        self.bot = bot
        self.l_clr = Colour.from_rgb(251, 85, 8)
        self.emote = self.bot.get_guild(716515460103012352)
        self.tick = get(self.emote.emojis, id=716606024450310174)
        self.warn = get(self.emote.emojis, id=716614609192222810)

    @commands.Cog.listener()
    async def on_ready(self):
        pass

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        if message.author == self.bot.user:
            return
        channel = get(message.author.guild.channels, name="logs"
                      )

        deleted = Embed(
            description=f"Message deleted in {message.channel.mention}", color=self.l_clr
        ).set_author(name=message.author, url=Embed.Empty, icon_url=message.author.avatar_url)

        deleted.add_field(name="Message", value=message.content)
        deleted.timestamp = message.created_at
        await channel.send(embed=deleted)

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        if before.author == self.bot.user:
            return

        channel = get(before.author.guild.channels, name="logs")

        edited = Embed(
            description=f"Message edited in {before.channel.mention} [Jump]({after.jump_url})", color=self.l_clr
        ).set_author(name=before.author, url=Embed.Empty, icon_url=before.author.avatar_url)
        if before.content and after.content:
            edited.add_field(name="Before", value=before.content, inline=False)
            edited.add_field(name="After", value=after.content, inline=False)
            edited.timestamp = after.created_at
        if edited.fields is not Embed.Empty:
            await channel.send(embed=edited)

    @commands.Cog.listener()
    async def on_message(self, message):
        if 'discord.gg/' in message.content:
            for perm, value in message.author.guild_permissions:
                if value and perm == 'manage_messages':
                    return
            await message.delete(delay=1)
            await message.channel.send(f"Invite links is chat is disabled! {self.warn}")

    @commands.Cog.listener()
    async def on_invite_create(self, invite):
        channel = get(invite.guild.channels, name="logs")
        invited = Embed().set_author(name=invite.inviter, url=Embed.Empty, icon_url=invite.inviter.avatar_url)
        invited.timestamp = invite.created_at
        invited.description = invite.url
        invited.color = self.l_clr
        invited.add_field(name="Channel", value=invite.channel.mention, inline=True)
        use = invite.max_uses
        if use == 0:
            use = "♾️"
        invited.add_field(name="Max Uses", value=use, inline=True)
        age = invite.max_age
        if age == 0:
            age = "♾️"
        else:
            age = f"{int(age / 3600)} hr"
        invited.add_field(name="Expiry", value=age, inline=True)
        await channel.send(embed=invited)

    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        channel = get(before.guild.channels, name="logs")
        old = before.roles
        new = after.roles
        rolechange = Embed().set_author(name=before, url=Embed.Empty, icon_url=before.avatar_url)
        try:
            if len(old) > len(new):
                role = [x for x in old if x not in new][0]
                rolechange.description = f"Removed role `{role}`"
            else:
                role = [x for x in new if x not in old][0]
                rolechange.description = f"Added role `{role}`"
        except IndexError:
            return
        rolechange.color = self.l_clr
        rolechange.timestamp = dt.now()
        await channel.send(embed=rolechange)

    @commands.group()
    @commands.has_permissions(manage_guild=True, manage_messages=True)
    async def revoke(self, ctx):
        if ctx.invoked_subcommand is None:
            for invite in await ctx.guild.invites():
                await invite.delete()
            await ctx.send(f'Revoked Invites for {ctx.guild.name}', delete_after=2)

    @revoke.group()
    async def by(self, ctx, member: Member):
        for invite in await ctx.guild.invites():
            if invite.inviter == member:
                await invite.delete()
        await ctx.send(f'Revoked Invites for {ctx.guild.name} by {member.display_name}', delete_after=2)

    @commands.group(invoke_without_command=True)
    @commands.has_permissions(manage_roles=True)
    async def color(self, ctx, name: str, code: str = None):
        if ctx.invoked_subcommand is None:
            if code is None:
                await ctx.send(embed=Embed(
                    title="Color picker tool", color=self.l_clr,
                    description="Pick the hex code for your color here",
                    url='https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_Colors/Color_picker_tool'
                ).set_thumbnail(url='https://developer.mozilla.org/static/img/opengraph-logo.72382e605ce3.png'))
                return
            code = code.strip("#")
            code = tuple(int(code[i:i + 2], 16) for i in (0, 2, 4))
            clr = Colour.from_rgb(*code)
            await ctx.message.add_reaction(self.tick)
            role = get(ctx.guild.roles, name=name)
            if role is not None:
                await role.edit(color=clr)
                await ctx.send(embed=Embed(
                    title=f"Edited Role {name} to {clr}", color=clr, timestamp=dt.now()
                ))
                return
            await ctx.guild.create_role(name=name, colour=clr)
            await ctx.send(embed=Embed(
                title=f"Created Role {name} of {clr}", color=clr, timestamp=dt.now()
            ))

    @color.group(invoke_without_command=True)
    async def give(self, ctx, member: Member, role: Role):
        await member.add_roles(role)
        await ctx.message.add_reaction(self.tick)
        await ctx.send(embed=Embed(
            title=f"Added Role {role} to {member.display_name}", color=role.color, timestamp=dt.now()
        ))

    @color.group(invoke_without_command=True)
    async def remove(self, ctx, member: Member, role: Role):
        await member.remove_roles(role)
        await ctx.message.add_reaction(self.tick)
        await ctx.send(embed=Embed(
            title=f"Removed Role {role} from {member.display_name}", color=role.color, timestamp=dt.now()
        ))

    @commands.command()
    @commands.has_role("Dev")
    async def invite(self, ctx, member: commands.Greedy[Member]):
        guild = ctx.guild

        channel = get(guild.channels, name="testing")
        await channel.set_permissions(guild.default_role, read_messages=False)
        for m in member:
            await channel.set_permissions(m, read_messages=True)
        await ctx.message.add_reaction(self.tick)

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def init(self, ctx):
        guild = ctx.guild
        category = get(guild.categories, name="Text Channels")
        basic = ["welcome", "rules", "testing", "logs"]
        for channel in basic:
            await guild.create_text_channel(channel, category=category)
        await ctx.send("Added text channels", delete_after=2)
        await ctx.message.delete(delay=3)

    @commands.command()
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def stats(self, ctx):
        guild: Guild = ctx.guild
        member: Member
        countb, counth, onlineb, onlineh = 0, 0, 0, 0
        for member in guild.members:
            if not member.bot:
                counth += 1
                if member.status in [Status.online, Status.idle]:
                    onlineh += 1
            else:
                countb += 1
                if member.status in [Status.online, Status.idle]:
                    onlineb += 1

        tchannels = ctx.guild.text_channels
        vchannels = ctx.guild.voice_channels

        stat = Embed()

        load = get(self.emote.emojis, id=716609458523865129)
        stat.title = f"{guild.name} {load}"
        stat.add_field(name=f"Members {counth}", value=f"{onlineh}/{counth} online", inline=True)
        stat.add_field(name=f"Bots {countb}", value=f"{onlineb}/{countb} online", inline=True)
        stat.add_field(name=f"Channels", value=f"{len(tchannels)} Text, {len(vchannels)} Voice", inline=True)
        stat.set_thumbnail(url=guild.icon_url)
        await ctx.send(embed=stat)


def setup(bot):
    bot.add_cog(Log(bot))
