from discord.ext import commands
from discord import Embed, Color
from beem.account import Account


class BlockChain(commands.Cog):
    """Blockchain info
    """

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='acc', aliases=['account'])
    async def _account(self, ctx, name):
        account = Account(name)
        bc = Embed(color=Color.green())
        bc.set_author(name=account.name)
        bc.add_field(name="Total Power", value=account.tp, inline=True)
        bc.add_field(name="Voting Power", value=account.vp, inline=True)
        c = account.get_creator()
        bc.add_field(name="Creator", value=c or "None", inline=True)
        bal = account.get_balances()
        bal = bal['available']
        bal = f"Available:\n{bal[0]}\n{bal[1]}\n{bal[2]}"
        bc.add_field(name="Balance", value=f"```{bal}```", inline=True)
        bc.add_field(name="Reputation", value=account.rep, inline=True)
        print(account.json_metadata)
        return await ctx.send(embed=bc)


def setup(bot):
    bot.add_cog(BlockChain(bot))
