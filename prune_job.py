from discord.ext import commands
from discord.errors import LoginFailure
from dotenv import load_dotenv
from os import getenv
from discord import Guild

load_dotenv()
# load the .env file


bot = commands.Bot(
    command_prefix=f"{getenv('BOT_PREFIX')}")


@bot.listen('on_ready')
async def print_stats():
    guild = bot.get_guild(618270738247581706)
    guild : Guild
    channel = guild.get_channel(677129130155704320)
    role = guild.get_role(621382663173046283)
    pruned = await guild.prune_members(days=14, reason='[Auto-Prune] Inactive', roles=[role])
    await channel.send(f"Pruned {pruned} members")
    await bot.logout()

if __name__ == '__main__':
    token = getenv('BOT_TOKEN')
    try:
        bot.run(token)
    except LoginFailure:
        print("Improper Token was passed!")
