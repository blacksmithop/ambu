from discord.ext import commands
from discord import Embed, File, Status, Member, Guild
from discord.utils import get


def setup(bot):
    bot.add_cog(Info(bot))


class Info(commands.Cog):
    """
    A module to provide information about Users, Bot and Guilds
    """

    def __init__(self, bot):
        self.bot = bot

    # check ping
    @commands.command(name='ping',
                      help='Get Discord Websocket Latency',
                      usage='.kping')
    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.bot_has_permissions(embed_links=True)
    async def _ping(self, ctx):
        ping_embed = Embed()
        file = File("static/ping.png", filename="ping.png")
        ping_embed.set_thumbnail(url="attachment://ping.png")
        ping_embed.add_field(name='Discord ', value=f'{round(self.bot.latency, 3)}s')
        await ctx.send(embed=ping_embed, file=file)

    # self roles
    @commands.command(name='dis',
                      aliases=['role', 'selfrole'],
                      help="Get a district role, may only have one role at a time",
                      usage=""".kdis [district]
                      \n.kdis \n-shows a list of district roles
                      \n.kdis KNR\n-Get the role for Kannur (KNR)
                      """)
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def _dis(self, ctx, role: str = None):
        member = ctx.author
        file = File("static/map.png", filename="map.png")

        role = get(ctx.guild.roles, name=role)
        s_roles = ['KSD', 'KNR', 'WYD', 'KZK', 'PKD', 'TSR', 'EKM', 'IDK', 'KTM', 'ALP', 'MLP', 'PTA', 'KLM', 'TVM']
        s_roles = [get(ctx.guild.roles, name=r) for r in s_roles]

        r_act = Embed(color=0x4287f5)
        r_act.set_thumbnail(url="attachment://map.png")
        if role is None or role not in s_roles:
            r_act.title = f"Self-roles for {ctx.guild.name}"
            r_act.description = ' '.join([r.name for r in s_roles])
            await ctx.send(embed=r_act, file=file)
            return

        mem_roles = [i for i in ctx.author.roles]
        c_role = list(set(s_roles) & set(mem_roles))

        if len(c_role) == 1:
            com = c_role[0].name
            if role.name == com:
                r_act.description = f"⛔ {member.mention}, already has role {role.mention}"
                await ctx.send(embed=r_act, file=file)
                return
            else:
                rem_role = get(ctx.guild.roles, name=com)
                await member.remove_roles(rem_role)
                await member.add_roles(role)
                r_act.description = f"⛔ Removed role {rem_role.mention} from {member.mention}\n\n✅ Replaced with {role.mention}"
                await ctx.send(embed=r_act, file=file)

        elif len(c_role) == 0:
            await member.add_roles(role)
            r_act.description = f"✅ Added role {role.mention} to {member.mention}"
            await ctx.send(embed=r_act, file=file)

    @commands.command(name="stats",
                      aliases=['guild', 'server'],
                      help="Get information about the server",
                      usage=""".kstats""")
    @commands.cooldown(1, 10, commands.BucketType.guild)
    async def stats(self, ctx):

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
        info = f"{humans}\n<:online:716606185868099664>{online}\n<:idle:716606098383306772>{idle}\n<:dnd:717626675193577533>{dnd}\n<:offline:716606306223652886>{offline}"
        stat = Embed(color=0x40EC96)
        stat.title = f"{guild.name}"
        stat.add_field(name="Members", value=info, inline=True)
        stat.add_field(name="Bots", value=f"{bots}", inline=True)
        stat.add_field(name="Channels",
                       value=f"{len(tchannels)} <:script:716617821152346194>, {len(vchannels)} <:vc:717635140167139370>",
                       inline=True)
        stat.add_field(name="Owner", value=guild.owner, inline=True)
        stat.add_field(name="Region", value=str(guild.region).title(), inline=True)
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
