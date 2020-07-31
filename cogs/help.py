from discord.ext import commands
from discord import Embed, Color
import db
from discord.utils import get
from aiohttp import ClientSession
from dotenv import load_dotenv
from os import getenv as e

load_dotenv()


def setup(bot):
    bot.add_cog(Help(bot))


class Help(commands.Cog):
    """Help command.
    """

    def __init__(self, bot):
        self.bot = bot
        bot.remove_command("help")
        self.db = db.BotConfig()
        self.guild = self.bot.get_guild(self.db.fetch(name="emote"))
        self.tick = get(self.guild.emojis, name="loading")
        self.client = get(self.guild.emojis, name="client")
        self.wumpus = get(self.guild.emojis, name="wumpus")
        self.bugs = get(self.guild.emojis, name="bugs")
        self.exec = get(self.guild.emojis, name="dev")
        self.pin = get(self.guild.emojis, name="pin")

    @commands.group(pass_context=True)
    async def help(self, ctx, cog: str = None):
        p = self.db.getprefix(id=ctx.guild.id) or '?'
        if cog is None:
            info = Embed(title='Cogs',
                         description=f'Use {p}help cog for more', color=Color.blue())
            info.set_footer(text="🧡", icon_url=ctx.author.avatar_url)
            info.timestamp = ctx.message.created_at
            info.set_author(name=self.bot.user.display_name,
                            url="https://blacksmithop.github.io/",
                            icon_url=self.bot.user.avatar_url)
            cogs = {"🎶 Music": "Music commands",
                    "📷 Fun": "Fun commands",
                    "💸 Economy": "Economy commands",
                    "🛠 Admin": "Commands for admins",
                    f"{self.wumpus} Settings ": "Bot settings",
                    f"{self.exec} Game": "Play games",
                    "🔞 NSFW": "NSFW commands",
                    f"{self.pin} Misc": "Other commands",
                    "🔍 Search": "Commands to search"
                    }
            for cog in cogs:
                info.add_field(name=cog, value=f'```{cogs[cog]}```')
            return await ctx.send(embed=info)

        curl = f"https://api.npoint.io/{e('HELP')}/"
        async with ClientSession() as session:
            resp = await session.get(url=f"{curl}/cogs")
            cogs = await resp.json()
        if cog in cogs:
            cog2cmd = Embed(title=cog,
                            description=f'Use {p}help command for more', color=Color.blue())
            cog2cmd.set_footer(text="🧡", icon_url=ctx.author.avatar_url)
            cog2cmd.timestamp = ctx.message.created_at
            cog2cmd.set_author(name=self.bot.user.display_name,
                               url="https://blacksmithop.github.io/",
                               icon_url=self.bot.user.avatar_url)
            async with ClientSession() as session:
                resp = await session.get(url=f"{curl}/{cog}")
                cogs = await resp.json()
            des = ', '.join(cogs)
            cog2cmd.description = f"```{des}```"
            return await ctx.send(embed=cog2cmd)
        curl = f"https://api.npoint.io/{e('HELP2')}/"

        async with ClientSession() as session:
            resp = await session.get(url=f"{curl}/{cog}")
            subcmd = await resp.json()
        if subcmd:
            subc = Embed(title=cog,
                         description=f'Use {p}help command for more', color=Color.blue())
            subc.set_footer(text="🧡", icon_url=ctx.author.avatar_url)
            subc.timestamp = ctx.message.created_at
            subc.set_author(name=self.bot.user.display_name,
                            url="https://blacksmithop.github.io/",
                            icon_url=self.bot.user.avatar_url)
            subc.add_field(name="Description", value=f"```{subcmd['des']}```")
            subc.add_field(name="Use", value=f"```{subcmd['use'].format(p=p)}```")
            subc.add_field(name="Permission", value=f"`{subcmd['perm']}`")
            subc.add_field(name="Alias", value=f"`{subcmd['alias']}`")
            subc.add_field(name="Cooldown", value=f"`{subcmd['cd']}`")
            return await ctx.send(embed=subc)
        else:
            return await ctx.send(embed=Embed(title=f'`{cog}` was not found {self.bugs}',
                                              description='[All Commands](https://blacksmithop.github.io/)',
                                              color=Color.red()))
