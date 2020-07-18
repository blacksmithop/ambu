from discord.ext import commands
from discord import Embed, Member, Colour, Role, Status, Guild
from discord.utils import get
from datetime import datetime as dt
from db import BotConfig
from better_profanity import profanity
from re import sub


class Log(commands.Cog):
    """Logging system.
    """

    def __init__(self, bot):
        self.bot = bot

        self.db = BotConfig()
        self.guild = self.bot.get_guild(self.db.fetch(name="emote"))
        self.tick = get(self.guild.emojis, name="agree")
        self.warn = get(self.guild.emojis, name="muted")
        self.load = get(self.guild.emojis, name="loading")

    def pid(self, id: int):
        return int(sub("[<#>]", '', id))

    @commands.Cog.listener()
    async def on_member_join(self, member):
        channel = self.db.getchannel(id=member.guild.id, channel="welcome")
        if not channel['channel']:
            return
        cnl = get(member.guild.channels, id=self.pid(channel['channel']))
        if not channel['message']:
            channel['message'] = "Welcome {member] to {server}"
        if not channel['information']:
            channel['infromation'] = "Follow the rules and have a good time!"
        title=channel["message"].format(member=member.mention, server=member.guild.name)
        description=channel["information"]
        await cn1.send(f"{title}\n{description}")

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        channel = self.db.getchannel(id=member.guild.id, channel="leave")
        if not channel['channel']:
            return
        cnl = get(member.guild.channels, id=self.pid(channel['channel']))
        if not channel['message']:
            channel['message'] = "Bye {member}"
        await cnl.send(embed=Embed(
            title=channel["message"].format(member=member.display_name), color=0x8722EB
        ).set_author(icon_url=member.avatar_url, name=member.display_name))

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        if message.author == self.bot.user:
            return

        channel = self.db.getchannel(id=message.guild.id, channel="logs")
        if not channel['channel']:
            return
        if not channel['delete']:
            return
        channel = get(message.guild.channels, id=self.pid(channel['channel']))
        deleted = Embed(
            description=f"Message deleted in {message.channel.mention}", color=0x4040EC
        ).set_author(name=message.author, url=Embed.Empty, icon_url=message.author.avatar_url)

        deleted.add_field(name="Message", value=message.content)
        deleted.timestamp = message.created_at
        await channel.send(embed=deleted)

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        if before.author == self.bot.user:
            return

        channel = self.db.getchannel(id=before.guild.id, channel="logs")
        if not channel['channel']:
            return
        if not channel['edit']:
            return
        channel = get(before.guild.channels, id=self.pid(channel['channel']))
        edited = Embed(
            description=f"Message edited in {before.channel.mention} [Jump]({after.jump_url})", color=0x9640EC
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
            if message.author == self.bot.user:
                return
            rem = self.db.getfilter(id=message.guild.id, filter="invite")
            if not rem:
                return
            await message.delete()
            await message.channel.send(f"Invite links not allowed in chat! {self.warn}")

        elif profanity.contains_profanity(message.content):
            if message.channel.is_nsfw():
                return
            c = self.db.getfilter(id=message.guild.id, filter="swear")
            if c:
                await message.delete()

    @commands.Cog.listener()
    async def on_invite_create(self, invite):

        channel = self.db.getchannel(id=invite.guild.id, channel="logs")
        if not channel['channel']:
            return
        if not channel['invite']:
            return
        channel = get(invite.guild.channels, id=self.pid(channel['channel']))
        invited = Embed().set_author(name=invite.inviter, url=Embed.Empty, icon_url=invite.inviter.avatar_url)
        invited.timestamp = invite.created_at
        invited.description = invite.url
        invited.color = 0x96EC40
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
        channel = self.db.getchannel(id=before.guild.id, channel="logs")
        if not channel['channel']:
            return
        if not channel['role']:
            return
        channel = get(before.guild.channels, id=self.pid(channel['channel']))
        if not channel:
            return
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
        rolechange.color = 0xEC4096
        rolechange.timestamp = dt.now()
        await channel.send(embed=rolechange)

    @commands.command()
    @commands.has_permissions(manage_guild=True, manage_messages=True)
    async def revoke(self, ctx, member: Member = None):
        """
        Revoke invites
        ?revoke
        or to revoke for a member
        ?revoke member
        """
        if member:
            for invite in await ctx.guild.invites():
                if invite.inviter == member:
                    await invite.delete()
            await ctx.send(embed=Embed(title=f'Revoked invites for {ctx.guild.name} by {member.display_name}'
                                       , color=0xDFDF2E))
            return
        for invite in await ctx.guild.invites():
            await invite.delete()
        await ctx.send(embed=Embed(title=f'Revoked all invites for {ctx.guild.name}'
                                   , color=0xDFDF2E))

    @commands.group(invoke_without_command=True)
    @commands.has_permissions(manage_roles=True)
    async def color(self, ctx, name: str, code: str = None):
        """
        Create a color role
        ?color name Hex
        """
        if ctx.invoked_subcommand is None:
            if code is None:
                await ctx.send(embed=Embed(
                    title="Color picker tool", color=0xfc4e03,
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
    async def add(self, ctx, member: Member, role: Role):
        """
        Adds a color role
        ?color add member name
        """
        await member.add_roles(role)
        await ctx.message.add_reaction(self.tick)
        await ctx.send(embed=Embed(
            title=f"Added Role {role} to {member.display_name}", color=role.color, timestamp=dt.now()
        ))

    @color.group(invoke_without_command=True)
    async def remove(self, ctx, member: Member, role: Role):
        """
        Removes a color role
        ?color remove member name
        """
        await member.remove_roles(role)
        await ctx.message.add_reaction(self.tick)
        await ctx.send(embed=Embed(
            title=f"Removed Role {role} from {member.display_name}", color=role.color, timestamp=dt.now()
        ))

    @commands.command()
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def stats(self, ctx):
        """
        Shows the stats for a Server
        ?stats
        """
        guild: Guild = ctx.guild
        member: Member
        bots, humans, online, idle, dnd, offline = 0, 0, 0, 0, 0, 0
        for member in guild.members:
            if not member.bot:
                humans += 1
                if member.status == Status.online:
                    online += 1
                if member.status == Status.offline:
                    offline += 1
                if member.status == Status.idle:
                    idle += 1
                if member.status == Status.dnd:
                    dnd += 1
            else:
                bots += 1

        tchannels = guild.text_channels
        vchannels = guild.voice_channels
        info = f"{humans}\n{get(self.guild.emojis, name='online')}{online}\n{get(self.guild.emojis, name='idle')}{idle}\n{get(self.guild.emojis, name='dnd')}{dnd}\n{get(self.guild.emojis, name='offline')} {offline}"
        stat = Embed()
        stat.color = 0x40EC96
        stat.title = f"{guild.name} {self.load}"
        stat.add_field(name="Members", value=info, inline=True)
        stat.add_field(name="Bots", value=f"{bots}", inline=True)
        stat.add_field(name="Channels",
                       value=f"{len(tchannels)} {get(self.guild.emojis, name='script')}, {len(vchannels)} {get(self.guild.emojis, name='vc')}",
                       inline=True)
        stat.add_field(name="Owner", value=guild.owner, inline=True)
        stat.add_field(name="Region", value=guild.region, inline=True)
        stat.add_field(name="Roles", value=f"{len(guild.roles)}", inline=True)

        emojitext = ""
        emojicount = 0
        for emoji in guild.emojis:
            if emoji.animated:
                emojiMention = "<a:" + emoji.name + ":" + str(emoji.id) + ">"
            else:
                emojiMention = "<:" + emoji.name + ":" + str(emoji.id) + ">"
            test = emojitext + emojiMention
            if len(test) > 1024:
                emojicount += 1
                if emojicount == 1:
                    ename = "Emojis ({:,} total)".format(len(guild.emojis))
                else:
                    ename = "Emojis (Continued)"
                stat.add_field(name=ename, value=emojitext, inline=True)
                emojitext = emojiMention
            else:
                emojitext = emojitext + emojiMention

        if len(emojitext):
            if emojicount == 0:
                emojiname = "Emojis ({} total)".format(len(guild.emojis))
            else:
                emojiname = "Emojis (Continued)"
            stat.add_field(name=emojiname, value=emojitext, inline=True)
        stat.set_thumbnail(url=guild.icon_url)
        stat.set_footer(text="Created at", icon_url=self.bot.user.avatar_url)
        stat.timestamp = guild.created_at
        await ctx.send(embed=stat)


def setup(bot):
    bot.add_cog(Log(bot))
