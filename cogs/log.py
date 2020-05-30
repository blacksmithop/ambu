from discord.ext import commands
from discord import Embed, Member, Colour, Role
from discord.utils import get
from datetime import datetime as dt


class Log(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.l_clr = Colour.from_rgb(251, 85, 8)

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
            description=f"Message deleted in {message.channel.mention}",color=self.l_clr
        ).set_author(name=message.author, url=Embed.Empty, icon_url=message.author.avatar_url)

        deleted.add_field(name="Message", value=message.content)
        deleted.timestamp = message.created_at
        await channel.send(embed=deleted)

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        if before.author == self.bot.user:
            return

        channel = get(before.author.guild.channels, name="logs"
                      )
        edited = Embed(
            description=f"Message edited in {before.channel.mention} [Jump]({after.jump_url})",color=self.l_clr
        ).set_author(name=before.author, url=Embed.Empty, icon_url=before.author.avatar_url)
        edited.add_field(name="Before", value=before.content, inline=False)
        edited.add_field(name="After", value=after.content, inline=False)
        edited.timestamp = after.created_at
        await channel.send(embed=edited)

    @commands.Cog.listener()
    async def on_message(self, message):
        if 'discord.gg/' in message.content:
            for perm, value in message.author.guild_permissions:
                if value and perm == 'manage_messages':
                    return
            await message.delete(delay=1)

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
        if len(old) > len(new):
            role = [x for x in old if x not in new][0]
            rolechange.description = f"Removed role `{role}`"
        else:
            role = [x for x in new if x not in old][0]
            rolechange.description = f"Added role `{role}`"
        rolechange.color = self.l_clr
        rolechange.timestamp = dt.now()
        await channel.send(embed=rolechange)

    @commands.group()
    @commands.has_permissions(manage_guild=True, manage_messages=True)
    async def revoke(self, ctx):
        if ctx.invoked_subcommand is None:
            for invite in await ctx.guild.invites():
                await invite.delete()
            rev = await ctx.send(f'Revoked Invites for {ctx.guild.name}')
            await rev.delete(delay=2)

    @revoke.group()
    async def by(self, ctx, member: Member):
        for invite in await ctx.guild.invites():
            if invite.inviter == member:
                await invite.delete()
        rev = await ctx.send(f'Revoked Invites for {ctx.guild.name} by {member.display_name}')
        await rev.delete(delay=2)

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
        await ctx.send(embed=Embed(
            title=f"Added Role {role} to {member.display_name}", color=role.color, timestamp=dt.now()
        ))

    @color.group(invoke_without_command=True)
    async def remove(self, ctx, member: Member, role: Role):
        await member.remove_roles(role)
        await ctx.send(embed=Embed(
            title=f"Removed Role {role} from {member.display_name}", color=role.color, timestamp=dt.now()
        ))

    @commands.command()
    @commands.has_role("Dev")
    async def invite(self, ctx, member: Member):
        guild = ctx.guild
        dev_role = get(guild.roles, name="Dev")
        channel = get(guild.channels, name="testing")
        await channel.set_permissions(guild.default_role, read_messages=False)
        await channel.set_permissions(member, read_messages=True)
        await channel.set_permissions(dev_role, read_messages=True, embed_links=True)


def setup(bot):
    bot.add_cog(Log(bot))
