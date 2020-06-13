from discord.ext import commands
from discord import Embed, Member
from asyncio import TimeoutError


class Poll(commands.Cog):
    """Error handling.
    """

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def poll(self, ctx):
        member = ctx.author
        member: Member
        maker = []
        await ctx.send("```What is the Question ❓```")
        em = ["🧪", "🧬", "🚀", "🖌️", "🧨"]

        def mcheck(m):
            return m.author == member

        try:
            msg = await self.bot.wait_for('message', timeout=20.0, check=mcheck)
            maker.append(msg.content)
        except TimeoutError:
            return await ctx.send("```Poll timed out ⏳```")

        await ctx.send("```How many options do you want?```")
        try:
            msg = await self.bot.wait_for('message', timeout=20.0, check=mcheck)
        except TimeoutError:
            return await ctx.send("```Poll timed out ⏳```")

        i = int(msg.content)
        if i > 20:
            return await ctx.send("```A maximum of 20 options for polls```")
        await ctx.send("```Enter your options ✔```")
        for i in range(i):
            try:
                await ctx.send(f"```{i + 1}) ```")
                msg = await self.bot.wait_for('message', timeout=20.0, check=mcheck)
                maker.append(msg.content)
                await msg.add_reaction("✅")
            except TimeoutError:
                return await ctx.send("```Poll timed out ⏳```")
        poller = Embed(color=0x5EE34)
        poller.title = maker[0]
        des = ''
        for j in range(1, len(maker)):
            des += f"```{em[j - 1]} {maker[j]}```\n"
        poller.description = des
        pr = await ctx.send(embed=poller)
        for j in range(i + 1):
            await pr.add_reaction(em[j])

        def reac_check(r, u):
            return pr.id == r.message.id and r.emoji in em

        eopt = {e: 0 for e in em}
        while True:
            try:
                reaction, user = await self.bot.wait_for('reaction_add', timeout=20.0, check=reac_check)
                e = str(reaction.emoji)
            except TimeoutError:
                await ctx.send("```Poll Finished ✅```")
                break
            if e in eopt.keys() and user != self.bot.user:
                eopt[e] += 1

        eopt = {k: v for k, v in sorted(eopt.items(), key=lambda item: item[1], reverse=True)}
        most = next(iter(eopt))
        loc = em.index(most)
        poller.title = "Results 🏆"
        poller.description = f"```Folks chose 📜\n{maker[loc + 1]}```"
        return await ctx.send(embed=poller)


def setup(bot):
    bot.add_cog(Poll(bot))
