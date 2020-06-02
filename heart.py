from sys import exit
from discord.ext import commands
from discord import Embed
from os import getenv as e, listdir as l
from logging import basicConfig, error, ERROR
from discord.errors import LoginFailure
from discord.ext.commands.errors import ExtensionFailed

import sys
import os.path

sys.path.append(os.path.join(os.path.dirname(__file__), 'ambu/'))
from db import BotConfig

db = BotConfig()
basicConfig(format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S', level=ERROR)


def prefix(bot, message):
    p = db.get(id=message.guild.id, key="prefix")
    return [p, f'<@!{bot.user.id}> ', f'<@{bot.user.id}> '] or '?'


bot = commands.Bot(command_prefix=prefix, description='Multi-purpose Discord Bot', case_insensitive=True)

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


@bot.command()
async def unload(ctx, cog):
    """Unloads a Cog"""
    if not await bot.is_owner(ctx.author):
        return
    coglist = [i.lower() for i in bot.cogs]
    if cog in coglist:
        bot.unload_extension(f"cogs.{cog}")
        await ctx.message.add_reaction("✅")
        await ctx.send(embed=Embed(title=f"Unloaded Cog: {cog}", color=0xEA0E0E))


@bot.command()
async def reload(ctx, cog):
    """Reloads a Cog"""
    if not await bot.is_owner(ctx.author):
        return
    coglist = [i.lower() for i in bot.cogs]
    if cog in coglist:
        await ctx.message.add_reaction("✅")
        bot.unload_extension(f"cogs.{cog}")
        bot.load_extension(f"cogs.{cog}")
        await ctx.send(embed=Embed(
            title=f"Reloaded Cog: {cog}", color=0xEA0E0E
        ))


@bot.command()
async def load(ctx, cogout):
    """Loads a Cog"""
    if not await bot.is_owner(ctx.author):
        return
    for cog in l("cogs"):
        if ".py" in cog:
            cogin = cog.replace(".py", "")
            if cogin == cogout:
                await ctx.message.add_reaction("✅")
                bot.load_extension(f"cogs.{cogin}")
                await ctx.send(embed=Embed(
                    title=f"Loaded Cog: {cogin}", color=0xEA0E0E
                ))


if __name__ == '__main__':
    try:
        bot.run(token)

    except LoginFailure:
        error("Token is Invalid")
