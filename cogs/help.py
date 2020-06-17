from discord import Embed, Color
from discord.ext import commands
from db import BotConfig
from discord.utils import get


class Help(commands.Cog):
    """Help command.
    """

    def __init__(self, bot):
        self.bot = bot
        bot.remove_command("help")
        self.db = BotConfig()
        self.guild = self.bot.get_guild(self.db.fetch(name="emote"))
        self.tick = get(self.guild.emojis, name="loading")
        self.client = get(self.guild.emojis, name="client")
        self.wumpus = get(self.guild.emojis, name="wumpus")
        self.bugs = get(self.guild.emojis, name="bugs")
        self.exec = get(self.guild.emojis, name="dev")
        self.pin = get(self.guild.emojis, name="pin")

    @commands.command(pass_context=True)
    async def help(self, ctx, *cog):
        """
        Shows the Help Command
        """
        p = self.db.getprefix(id=ctx.guild.id) or '?'
        try:
            if not cog:
                info = Embed(title='Cogs',
                             description=f'Use {p}help cog for more', color=Color.blue())
                info.set_footer(text="🧡", icon_url=ctx.author.avatar_url)
                info.timestamp = ctx.message.created_at
                info.set_author(name=self.bot.user.display_name,
                                url="https://blacksmithop.github.io/",
                                icon_url=self.bot.user.avatar_url)
                cogs = {"🛠 Admin": "Commands for admins",
                        "📷 Image": "Image commands",
                        "🎶 Music": "Music commands",
                        "🧾 Log": "Logging",
                        f"{self.wumpus} Settings ": "Bot settings",
                        "🎞 Movie": "Search for movies",
                        f"{self.pin} Poll": "Run a poll",
                        f"{self.exec} Game": "Play games",
                        }
                for cog in cogs:
                    info.add_field(name=f"**{cog}**", value=f"`{cogs[cog]}`", inline=True)

                await ctx.message.add_reaction(emoji='✅')
                await ctx.send('', embed=info)
            else:
                if len(cog) > 1:
                    info = Embed(title=self.bugs,
                                 description='Try the [Detailed Help](https://blacksmithop.github.io/)',
                                 color=Color.green())
                    await ctx.message.add_reaction(emoji='✅')
                    await ctx.send('', embed=info)
                else:
                    found = False
                    for x in self.bot.cogs:
                        for y in cog:
                            if x == y:
                                info = Embed(title=f'{cog[0]} Commands',
                                             description=self.bot.cogs[cog[0]].__doc__,
                                             color=Color.blurple())
                                for c in self.bot.get_cog(y).get_commands():
                                    if not c.hidden:
                                        info.add_field(name=c.name, value=c.help, inline=False)
                                found = True
                    if not found:
                        info = Embed(title=f'Cog `{cog[0]}` not found {self.bugs}',
                                     description='Try the [Detailed Help](https://blacksmithop.github.io/)',
                                     color=Color.red())
                    else:
                        await ctx.message.add_reaction(emoji='✅')
                    await ctx.send('', embed=info)
        except:
            await ctx.message.add_reaction(emoji='⛔')
            await ctx.send("Missing permission to send Embeds")


def setup(bot):
    bot.add_cog(Help(bot))
