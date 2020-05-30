from sys import exit
from discord.ext import commands
from os import environ as e, listdir as l
from logging import basicConfig, error, ERROR, info
from discord.errors import LoginFailure
from discord import Status, Game
from discord.ext.commands.errors import ExtensionFailed
from discord import Embed

basicConfig(format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S', level=ERROR)
bot = commands.Bot(command_prefix='?', description='Multi-purpose Discord Bot', case_insensitive=True)
try:
    token = e['DISCORD_TOKEN']
except KeyError:
    error("Token not found")
    exit()


@bot.event
async def on_ready():
    print(f"Logged in as: {bot.user.display_name}")
    await bot.change_presence(status=Status.online, activity=Game(name="?help"))
    for cog in l("cogs"):
        if ".py" in cog:
            cog = cog.replace(".py", "")
            try:
                bot.load_extension(f"cogs.{cog}")
            except ExtensionFailed:
                error(f"Failed to load {cog}")


@bot.event
async def on_command_error(ctx, error):
    """
    :type error: object
    """
    if isinstance(error, commands.CommandNotFound):
        msg = await ctx.send(embed=Embed(
            title=error.args[0]
        ))
        await ctx.message.delete(delay=2)
        await msg.delete(delay=2)


if __name__ == '__main__':
    try:
        bot.run(token)
    except LoginFailure:
        error("Token is Invalid")
