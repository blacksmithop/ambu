from discord.ext import commands
from discord import Embed
from db import BotConfig
from numpy import ones as o
from discord.utils import get
from asyncio import sleep, TimeoutError
from numpy import ones


class Game(commands.Cog):
    """Error handling.
    """

    def __init__(self, bot):
        self.bot = bot
        self.db = BotConfig()
        self.guild = self.bot.get_guild(self.db.fetch(name="emote"))
        self.join = get(self.guild.emojis, name="agree")
        self.leave = get(self.guild.emojis, name="muted")

    @commands.command()
    async def okp(self, ctx):
        members = set({})
        oram = Embed(title="💃 Oramma Kadayil Poyi 🌊", color=0xf79100, description="React to join the game 🐟")
        m = await ctx.send(embed=oram)
        await m.add_reaction(self.join)

        def check(r, u):
            return u != self.bot.user and r.emoji == self.join

        while True:
            try:
                await self.bot.wait_for(event="reaction_add", timeout=5, check=check)
            except TimeoutError:
                break
        msg = await ctx.channel.fetch_message(id=m.id)
        for reaction in msg.reactions:
            async for user in reaction.users():
                members.add(user)
        members.remove(self.bot.user)

        await ctx.send(embed=Embed(title="🔹 Players 🔸",
                                   description=f'\n'.join(m.display_name for m in members),
                                   color=0xf79100))

        def kkk(gb, rp, cp, n, num, rc):
            count = 0
            while True:
                cp += 1
                if cp > 4:
                    cp = 0
                    rp += 1
                    if rp >= n:
                        rp = 0
                if gb[rp, cp] == 1:
                    count += 1
                if count == num:
                    break
            if rc == 'r':
                return rp
            else:
                return cp

        def cg():
            for i in range(len(members)):
                count = 0
                for j in range(5):
                    if gb[i][j] == 0:
                        count += 1
                if count == 5:
                    return True
            return False

        rp, cp = 0, 0
        colors = []
        gb = ones((len(members), 5))
        print("GAME", gb)
        members = list(members)

        while True:
            r = rp
            rp = kkk(gb, rp, cp, len(members), 13, 'r')
            cp = kkk(gb, r, cp, len(members), 13, 'c')

            await ctx.send(embed=Embed(
                description="""Oramma kadayil poyi\n
                                Oru dazan vala vaangi\n
                                aa valayude niramenth?""",
                color=0xf79100))
            await ctx.send(f"**{members[rp].display_name}** :")

            def getcolor(m):
                return m.author == members[rp]

            try:
                msg = await self.bot.wait_for('message', check=getcolor, timeout=5)
                if msg.content not in colors:
                    colors.append(msg.content)
            except TimeoutError:
                await ctx.send("Player took too long, *exiting game.. *")
                return
            r = rp

            rp = kkk(gb, rp, cp, len(members), len(colors[-1]), 'r')
            cp = kkk(gb, r, cp, len(members), len(colors[-1]), 'c')
            print(r,rp,cp)
            gb[rp, cp] = 0
            status = ""

            for i in range(len(members)):
                status += f"{members[i].display_name}: |{' '.join(str(gb[i])[1:-1])}|\n"
            await ctx.send(embed=Embed(title="Board",
                                       description=f"```{status}```",
                                       color=0xf79100))
            if cg():
                break
            win = members[rp]
            r = rp
            rp = kkk(gb, rp, cp, len(members), 1, 'r')
            cp = kkk(gb, r, cp, len(members), 1, 'c')

        await ctx.send(embed=Embed(title="Game Over",
                                   description=f"{win.display_name} is the Winner", color=0xfc2403))


def setup(bot):
    bot.add_cog(Game(bot))
