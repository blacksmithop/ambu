from discord.ext import commands
from discord import Embed
from discord.utils import get

class Help(commands.Cog):
    """Help command.
    """

    def __init__(self, bot):
        self.bot = bot
        self.emote = self.bot.get_guild(716515460103012352)
        self.tick = get(self.emote.emojis, id=716926950857506846)
        self.client = get(self.emote.emojis, id=716927608876695603)
        #bot.remove_command("help")

    @commands.command()
    async def hlp(self, ctx, cog: str = None, sub: str = None):

        cogs = {"🛠 Config": "Configure the bot", "🧾 Log": "Setup logging", "📷 Image": "Image commands"}

        cogcmds = {"config": ["prefix", "purge", "mute", "unmute", "setchannel", "cogs", "disable"],
                   "log": ["color", "revoke", "invite", "stats", "init"],
                   "image": ["cat", "fox", "dog", "nature", "porn"]
                   }
        cmds = {
            "prefix": ["Shows the bot Prefix", 5, None, None, ["set", "mention"]],
            "purge": ["Deletes messages", 5, "manage_messages", "number[int]/ by mem[member] number[int]", None],
            "mute": ["Mutes a member", None, "manage_roles", "user[member] time[int] unit[s,m,h]", None],
            "unmute": ["Unmutes a member", None, "manage_roles", "user[member]", None],
            "cogs": ["Shows available Cogs", None, "is_owner", None, ["show", "load", "unload", "reload"]],
            "disable": ["Disables a Command", None, "is_owner", "command[cmd]", None],
            "setchannel": ["Configures channels", 10, "administrator", None, ["role"]],
            "color": ["Creates a color role", None, "manage_roles", "name[str] code[hex]", ["give", "remove"]],
            "revoke": ["Revokes all invite links", None, "manage_guild, manage_messages", ["/ by mem[member]"], None],
            "invite": ["Invites members to testing channel", None, "has_role Dev", "mem[member],mem2[member],...", None],
            "stats": ["Statistics about the server", 10, None, None, None],
            "init": ["Creates logging channels", None, "administrator", None, None]
        }

        subcmds = {
            "set": ["Sets the bot prefix", 5, "administrator", "new-prefix[str]"],
            "mention": ["Use bot by mention", 5, "administrator", None],
            "show": ["Shows loaded cogs", None, "is_owner", None],
            "load": ["Loads a cog", None, "is_owner","cog-name[str]"],
            "unload": ["Unloads a cog", None, "is_owner", "cog-name[str]"],
            "reload": ["Reloads a cog", 10, "is_owner", "cog-name[str]"],
            "role": ["Configures channel roles", 10, "administrator", None],
            "give": ["Adds color role to user", None, "manage_roles", "mem[member] role[str]"],
            "remove": ["Removes color role from user", None, "manage_roles", "mem[member] role[str]"]
        }
        hembed = Embed()
        hembed.set_author(name=self.bot.user.display_name,
                          url="https://github.com/blacksmithop/ambu",
                          icon_url=self.bot.user.avatar_url)
        hembed.set_footer(text="•", icon_url=ctx.author.avatar_url)
        hembed.timestamp = ctx.message.created_at

        if cog is None:
            hembed.title = f"Cogs {self.tick}"
            hembed.description = f"Do {self.bot.command_prefix}help [cog] for more information"
            for cog in cogs.keys():
                hembed.add_field(name=f"**{cog}**", value=f"`{cogs[cog]}`", inline=True)

        cog = cog.lower()
        if cog in cogcmds:
            hembed.title = f"Commands in {cog} {self.tick}"
            hembed.description = f"Do {self.bot.command_prefix}help [cmd] for more information"
            cmddes = ""
            for cmd in cogcmds[cog]:
                cmddes += f"`{cmd}` "
            hembed.add_field(name="Commands", value=cmddes)

        param = ["Description", "Cooldown", "Permission"]
        if cog in cmds and sub is None:
            hembed.title = f"Command {cog} {self.tick}"
            hembed.description = f"Do {self.bot.command_prefix}help [cmd] [subcmd] for more information"
            cmd = cmds[cog]
            i: int = 0
            for par in param:
                hembed.add_field(name=par, value=cmd[i], inline=True)
                i += 1
            if cmd[3] is not None:
                usage = f"`{self.bot.command_prefix}{cog} {cmd[3]}`"
            else:
                usage = f"`{self.bot.command_prefix}{cog}`"
            hembed.add_field(name="Usage", value=usage)

            scmds = ""
            if cmd[4] is not None:
                for c in cmd[4]:
                    scmds += f" `{c}`"
            if scmds == "":
                scmds = None

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
                    usage = f"`{self.bot.command_prefix}{cog} {sub} {subcmds[sub][3]}`"
                else:
                    usage = f"`{self.bot.command_prefix}{cog} {sub}`"
                hembed.add_field(name="Usage", value=usage)
        if hembed.title is Embed.Empty:
            if cog and sub is None:
                hembed.description = f"No cog/command named `{cog}` {self.client}"
            if sub:
                hembed.description = f"No sub-command `{sub}` under `{cog}` {self.client}"
        await ctx.send(embed=hembed)


def setup(bot):
    bot.add_cog(Help(bot))
