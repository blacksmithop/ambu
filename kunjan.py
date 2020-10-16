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
bot.remove_command('help')

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
