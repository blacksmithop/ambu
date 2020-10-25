from discord.ext import commands
from discord import Embed


def setup(bot):
    bot.add_cog(Help(bot))


class Help(commands.Cog):
    """
    A module to provide detailed information about Cogs, Commands and their Sub-Commands
    """
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='help', help="A command to provide detailed information about Cogs, Commands and their "
                                        "Sub-Commands",
                      usage=""".khelp [cog/command]\n\n.khelp\n-shows the list of cogs
                      \n.khelp Help\n-shows the commands under the cog Help
                      \n.khelp ping\n-shows information about the command ping
                      \n[argument] = optional\n"""
                      )
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def _help(self, ctx, argument: str = None):
        help_embed = Embed(color=0x000080)
        cogs = self.bot.cogs
        cmd = None

        if not argument:
            cogs = list(cogs.keys())
            cogs.remove('Help')
            help_embed.title = "List of Cogs"
            help_embed.description = f"```{', '.join(cogs)}```"
            return await ctx.send(embed=help_embed)

        if argument.lower() == 'help':
            cmd = self.bot.get_command('help')

        if argument.title() in cogs and cmd is None:
            help_embed.title = f'Cog: {argument.title()}'
            cog = cogs[argument.title()]
            cmds = cog.get_commands()
            cmds = [cmd.name for cmd in cmds]
            cmds = f"```{', '.join(cmds)}```"
            help_embed.add_field(name="Commands",
                                 value=cmds)
            return await ctx.send(embed=help_embed)

        else:
            cogs = list(cogs.values())
            if not cmd:
                for cog in cogs:
                    cog: commands.Cog

                    cmds = cog.get_commands()
                    cmd = next((cmd for cmd in cmds if cmd.name == argument), None)

            if not cmd:
                return await ctx.send(f'Could not find help for {argument}')
            cmd: commands.Command
            help_embed.title = f'Command: {cmd.name.title()}'
            help_embed.description = f'```{cmd.help}```'
            help_embed.add_field(name="Usage", value=f'```{cmd.usage}```')
            help_embed.add_field(name="Aliases", value=f"```{', '.join(cmd.aliases) if cmd.aliases else None}```")
            help_embed.add_field(name="Cooldown", value=f'```{int(cmd._buckets._cooldown.per)} s```')
            help_embed.add_field(name="Cog", value=f'```{cmd.cog.qualified_name}```')
            await ctx.send(embed=help_embed)

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if hasattr(error, 'on_error'):
            return
        else:
            raise error

    @commands.Cog.listener()
    async def on_command(self, ctx: commands.Context):
        if await self.bot.is_owner(ctx.author):
            command = ctx.command
            command.reset_cooldown(ctx=ctx)
