from sys import exit
from discord.ext import commands
from os import getenv as e, listdir as l
from logging import basicConfig, error, ERROR
from discord.errors import LoginFailure
from discord.ext.commands.errors import ExtensionFailed

basicConfig(format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S', level=ERROR)
bot = commands.Bot(command_prefix='?', description='Multi-purpose Discord Bot', case_insensitive=True)
try:
    token = e('token')
except KeyError:
    error("Token not found")
    exit()


@bot.event
async def on_ready():
    print(f"Logged in as: {bot.user.display_name}")
    for cog in l("cogs"):
        if ".py" in cog:
            cog = cog.replace(".py", "")
            try:
                bot.load_extension(f"cogs.{cog}")
            except ExtensionFailed:
                error(f"Failed to load {cog}")


if __name__ == '__main__':
    try:
        bot.run(token)

    except LoginFailure:
        error("Token is Invalid")