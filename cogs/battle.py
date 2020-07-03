from discord.ext import commands, tasks
from discord import Embed, Color, Member
from asyncio import sleep
from random import choice, randrange


async def get(session: object, url: object) -> object:
    async with session.get(url) as response:
        return await response.text()


class Battle(commands.Cog):
    """NYTimes
    """

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def battle(self, ctx, p2: Member):
        animals = {
            "elephant": "https://i.ibb.co/PChZn5G/ele.jpg",
            "mongoose": "https://i.ibb.co/dPdqKYG/mong.jpg",
            "monkey": "https://i.ibb.co/YPCt9pq/oran.jpg"
        }
        p1 = ctx.author
        game = Embed(color=Color.green())
        beast = list(animals.keys())
        p1 = [p1, choice(beast)]
        hp = randrange(100, 300)
        b1 = [hp, hp]
        game.set_author(name=p1[1].title(), icon_url=animals[p1[1]])
        game.description = f"{p1[0].display_name} goes to battle with a {p1[1].title()}!"
        game.set_footer(text=f"HP {b1[0]}/{b1[1]}", icon_url=p1[0].avatar_url)
        await ctx.send(embed=game)
        await sleep(2)
        p2 = [p2, choice(beast)]
        hp = randrange(100, 300)
        b2 = [hp, hp]
        game.set_author(name=p2[1].title(), icon_url=animals[p2[1]])
        game.description = f"{p2[0].display_name} goes to battle with a {p2[1].title()}!"
        game.set_footer(text=f"HP {b2[0]}/{b2[1]}", icon_url=p2[0].avatar_url)
        await ctx.send(embed=game)
        await sleep(2)
        battle = Embed(color=Color.red())
        battle.description = "**Battle Start**!"
        msg = await ctx.send(embed=battle)
        while b1[0] > 0 and b2[0] > 0:
            b1a = randrange(10, 50)
            b2a = randrange(10, 50)
            b1[0] -= b2a
            b2[0] -= b1a
            battle.set_author(name=p1[1].title(), icon_url=animals[p1[1]])
            log = f"{p1[0].display_name}'s {p1[1]} deals **{b1a}** damage!\n"
            log += f"HP **{b1[0]}**/**{b1[1]}**\n\n\n"
            log += f"{p2[0].display_name}'s {p2[1]} deals **{b2a}** damage!\n"
            log += f"HP **{b2[0]}**/**{b2[1]}**\n"
            battle.description = log
            battle.set_footer(text=p2[1].title(), icon_url=animals[p2[1]])
            await msg.edit(embed=battle)
            await sleep(3)
        win = p1 if b1[0] > b2[0] else p2
        result = Embed(color=Color.gold())
        result.title = f"🎉 {win[0].display_name} 🎉 won the battle! "
        result.set_thumbnail(url=animals[win[1]])
        await ctx.send(embed=result)


def setup(bot):
    bot.add_cog(Battle(bot))
