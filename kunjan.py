from discord.ext import commands
from discord import Embed, File, Status, Streaming, Intents
from discord.errors import LoginFailure
from dotenv import load_dotenv
from os import getenv, listdir

load_dotenv()
# load the .env file
intents = Intents.all()
intents.members = True

bot = commands.Bot(
    command_prefix=f"{getenv('BOT_PREFIX')}", intents=intents
)
bot.remove_command('help')

# for cogs
bot.load_extension('jishaku')
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
    await bot.change_presence(activity=Streaming(name=".khelp", url=getenv('TWITCH_URL')))


@bot.event
async def on_message(message):
    """Overloads the default on_message event to check for cache readiness"""
    if not bot.is_ready:
        return await message.add_reaction('<a:loading:716609458523865129>')

    await bot.process_commands(message)


@bot.event
async def on_member_join(member):
    if member.guild.id != 618270738247581706:
        return
    channel = member.guild.system_channel
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
