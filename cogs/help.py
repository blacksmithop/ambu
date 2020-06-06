from discord.ext import commands
from discord import Embed
from discord.utils import get
from ambu.db import BotConfig


class Help(commands.Cog):
    """Help command.
    """

    def __init__(self, bot):
        self.bot = bot
        self.db = BotConfig()
        self.guild = self.bot.get_guild(self.db.fetch(name="emote"))
        self.tick = get(self.guild.emojis, name="loading")
        self.client = get(self.guild.emojis, name="client")
        self.exec = get(self.guild.emojis, name="dev")
        self.server = get(self.guild.emojis, name="discord")
        self.wumpus = get(self.guild.emojis, name="wumpus")
        self.bugs = get(self.guild.emojis, name="bugs")
        bot.remove_command("help")

    @commands.command()
    async def help(self, ctx, cog: str = None, sub: str = None):
        prefix = self.db.getparam(id=ctx.guild.id, key=["prefix"])

        cogs = {"🛠 Admin": "Commands for admins",
                "📷 Image": "Image commands",
                "🧾 Log": "Logging",
                f"{self.wumpus} Settings ": "Bot settings",
                f"{self.exec} Repl": f"Python interpreter",
                f"{self.server} Server": "Web-server"
                }

        cogcmds = {"admin": ["purge", "mute", "unmute", "cogs"],
                   "log": ["color", "revoke", "invite", "stats", "init"],
                   "image": ["cat", "fox", "dog", "nature", "porn"],
                   "repl": ["jsk"],
                   "help": ["help"],
                   "settings": ["set", "info"]
                   }
        cmds = {
            "purge": ["Deletes messages", 5, "manage_messages", "limit member(optional)", None],
            "mute": ["Mutes a member", None, "manage_roles", "user time unit(s,m,h)", None],
            "unmute": ["Unmutes a member", None, "manage_roles", "user", None],
            "cogs": ["Shows available Cogs", None, "is_owner", None, ["all"]],
            "color": ["Creates a color role", None, "manage_roles", "name hex-code", ["give", "remove"]],
            "revoke": ["Revokes all invite links", None, "manage_guild, manage_messages", ["/ by user"], None],
            "invite": ["Invites members to testing channel", None, "has_role Dev", "user1, user2..", None],
            "stats": ["Statistics about the server", 10, None, None, None],
            "init": ["Creates logging channels", None, "administrator", None, None],
            "cat": ["Random cat image", None, None, None, None],
            "fox": ["Random fox image", None, None, None, None],
            "dog": ["Random dog image", None, None, None, None],
            "nature": ["Random nature image", None, None, None, None],
            "porn": ["Random nature image", None, "is_nsfw", None, None],
            "jsk": ["Run Python code", None, "is_owner", "```py\nfrom math import pi```", None],
            "help": ["Shows the help command", None, None, None, None],
            "info": ["Shows bot settings", None, None, None, None],
            "set": ["Set's bot configuration", None, "administrator", "[setting] [value]",
                    ["prefix", "welcome", "leave", "verification",
                     "roles", "logs", "maxwarns", "bans",
                     "testing", "spamfilter", "invitefilter", "cussfilter"]]
        }

        subcmds = {
            "add": ["Adds color role to user", None, "manage_roles", "mem [member] role [str]"],
            "remove": ["Removes color role from user", None, "manage_roles", "mem [member] role [str]"],
            "welcome": ["Welcomer settings", None, "administrator", "channel: #welcome |\nmessage: Welcome {member} |\ninformation Read the rules at #channel"],
            "leave": ["Farewell settings", None, "administrator", "channel: #leave |\nmessage: {member} has left"],
            "verification": ["Verification settings", None, "administrator", "channel: #welcome |\nmessage:Do __ to accept |"],
            "testing": ["Sets the testing channel", None, "administrator", "channel #channel"],
            "logs": ["Logging settings", None, "administrator", "channel"],
            "invitefilter": ["Allow / Disallow invite links", None, "administrator", "True | False"],
            "cussfilter": ["Allow / Disallow invite cussing", None, "administrator", "True | False"],
            "spamfilter": ["Allow / Disallow invite spam", None, "administrator", "True | False "],
            "maxwarns": ["Set maximum number of user warns", None, "administrator", None]
        }
        hembed = Embed()
        hembed.set_author(name=self.bot.user.display_name,
                          url="https://github.com/blacksmithop/ambu",
                          icon_url=self.bot.user.avatar_url)
        hembed.set_footer(text="🧡", icon_url=ctx.author.avatar_url)
        hembed.timestamp = ctx.message.created_at

        if cog is None:
            hembed.title = f"Cogs {self.tick}"
            hembed.description = f"Do {prefix}help [cog] for more information"
            for cog in cogs.keys():
                hembed.add_field(name=f"**{cog}**", value=f"`{cogs[cog]}`", inline=True)

        cog = cog.lower()
        if cog in cogcmds:
            hembed.title = f"Commands in {cog} {self.tick}"
            hembed.description = f"Do {prefix}help [cmd] for more information"
            cmddes = ""
            for cmd in cogcmds[cog]:
                cmddes += f"`{cmd}` "
            hembed.add_field(name="Commands", value=cmddes)

        param = ["Description", "Cooldown", "Permission"]
        if cog in cmds and sub is None:
            hembed.title = f"Command {cog} {self.tick}"
            cmd = cmds[cog]
            if cmd[4]:
                hembed.description = f"Do {prefix}help [cmd] [subcmd] for more information"
            i: int = 0
            for par in param:
                hembed.add_field(name=par, value=cmd[i], inline=True)
                i += 1
            if cmd[3] is not None:
                usage = f"`{prefix}{cog} {cmd[3]}`"
            else:
                usage = f"`{prefix}{cog}`"
            hembed.add_field(name="Usage", value=usage)

            scmds = ""
            if cmd[4] is not None:
                for c in cmd[4]:
                    scmds += f" `{c}`"
                hembed.add_field(name="Sub-commands", value=scmds)

        if sub:
            if sub in cmds[cog][4]:
                param = ["Description", "Cooldown", "Permission"]
                hembed.title = f"Sub-command {cog} {self.tick}"
                i: int = 0
                for par in param:
                    hembed.add_field(name=par, value=subcmds[sub][i])
                    i += 1
                if subcmds[sub][3] is not None:
                    usage = f"`{prefix}{cog} {sub} {subcmds[sub][3]}`"
                else:
                    usage = f"`{prefix}{cog} {sub}`"
                hembed.add_field(name="Usage", value=usage)
        if hembed.title is Embed.Empty:
            if cog and sub is None:
                hembed.description = f"No cog/command named `{cog}` {self.client}"
            if sub:
                hembed.description = f"No sub-command `{sub}` under `{cog}` {self.client}"
        await ctx.send(embed=hembed)


def setup(bot):
    bot.add_cog(Help(bot))
