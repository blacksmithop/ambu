from discord.ext import commands
from discord import Embed, Member, Status
import db
from discord.utils import get


class Economy(commands.Cog):
    """Error handling.
    """

    def __init__(self, bot):
        self.bot = bot
        self.db = db.BotConfig()
        self.guild = self.bot.get_guild(self.db.fetch(name="emote"))
        self.on = get(self.guild.emojis, name="online")
        self.off = get(self.guild.emojis, name="offline")
        self.idle = get(self.guild.emojis, name="idle")
        self.dnd = get(self.guild.emojis, name="dnd")

    @commands.command(name='balance', aliases=['bank', 'bal'])
    async def balance(self, ctx, member: Member = None):
        if member is None:
            member = ctx.author
        user = Embed(color=0x857272)
        user.set_author(name=member.display_name, icon_url=member.avatar_url)
        bal = self.db.getuser(uid=member.id)
        user.description = f"```Balance: {bal} 🥥```"
        user.timestamp = ctx.message.created_at
        await ctx.send(embed=user)

    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def user(self, ctx, member: Member = None):

        if member is None:
            member = ctx.author

        e2s = {
            Status.online: self.on,
            Status.offline: self.off,
            Status.idle: self.idle,
            Status.dnd: self.dnd

        }

        user = Embed(color=member.color)
        user.set_author(name=member)
        user.set_thumbnail(url=member.avatar_url)
        user.timestamp = ctx.message.created_at
        user.add_field(name="Status", value=e2s[member.status], inline=True)
        user.add_field(name="Joined", value=member.joined_at.strftime("%d-%m-%Y"), inline=True)
        user.add_field(name="Created", value=member.created_at.strftime("%d-%m-%Y"), inline=True)
        user.add_field(name="Nickname", value=member.display_name, inline=True)
        mob = "📱" if member.is_on_mobile() else "📵"
        user.add_field(name="Mobile", value=mob, inline=True)
        roles = member.roles
        user.add_field(name="Roles", value=', '.join([role.mention for role in roles]), inline=False)
        if member.status is Status.offline:
            return await ctx.send(embed=user)
        act = member.activities
        if act[0]:
            try:
                user.add_field(name="Activity 🍞", value=f"{act[0].emoji.name or ''} {act[0].name}", inline=True)
            except:
                user.add_field(name="Spotify 🎶", value=f"{act[0].title} by {act[0].artist}", inline=True)
        if act[1]:
            try:
                user.add_field(name="Spotify 🎶", value=f"{act[1].title} by {act[1].artist}", inline=True)
            except:
                try:
                    user.add_field(name="Custom 😎", value=f"{act[1].name}, {act[1].details}", inline=True)
                    if act[2]:
                        try:
                            user.add_field(name="Spotify 🎶", value=f"{act[2].title} by {act[2].artist}", inline=True)
                        except:
                            pass
                except:
                    pass
        await ctx.send(embed=user)


def setup(bot):
    bot.add_cog(Economy(bot))
