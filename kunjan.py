from discord.ext import commands
from discord import Embed, File, Status, Game, Intents
from discord.errors import LoginFailure
from dotenv import load_dotenv
from os import getenv, listdir
from discord.utils import get

load_dotenv()
# load the .env file
intents = Intents.default()
intents.members = True

bot = commands.Bot(
    command_prefix=f"{getenv('BOT_PREFIX') or '`'}", intents=intents
)

# for cogs
for cog in listdir('cog'):
    if '.py' not in cog:
        continue
    print(f"Loaded cog: {cog[:-3]}")
    bot.load_extension(f'cog.{cog[:-3]}')


@bot.listen('on_ready')
async def print_stats():
    print(f"Logged in as: {bot.user}")
    print(f"Shard-id: {bot.shard_id or 0}")
    print(f"Shards: {bot.shard_count or 0}")
    await bot.change_presence(status=Status.online, activity=Game(f"{bot.command_prefix}help"))


# check ping
@bot.command(name='ping')
@commands.bot_has_permissions(embed_links=True)
async def _ping(ctx):
    ping_embed = Embed()
    file = File("static/ping.png", filename="ping.png")
    ping_embed.set_thumbnail(url="attachment://ping.png")
    ping_embed.add_field(name='Discord ', value=f'{round(bot.latency, 3)}s')
    await ctx.send(embed=ping_embed, file=file)


# self roles
@bot.command(name='dis')
async def _dis(ctx, role: str = None):
    """
        Get a self role
        ?sr name
        """
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


@bot.event
async def on_member_join(member):
    channel = bot.get_channel(618270738247581708)
    welcome = Embed(color=0x9370db)
    file = File("static/banner.png", filename="banner.png")
    welcome.set_thumbnail(url="attachment://banner.png")
    welcome.title = f"Welcome {member.name} to {member.guild.name}"
    welcome.description = "Checkout <#621023138645278720> for rules and roles"
    await channel.send(embed=welcome, file=file)


if __name__ == '__main__':
    token = getenv('BOT_TOKEN')
    try:
        bot.run(token)
    except LoginFailure:
        print("Improper Token was passed!")
