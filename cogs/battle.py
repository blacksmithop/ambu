from discord.ext import commands
from discord import Embed, Color, Member
from asyncio import sleep
from random import choice, randrange


animals = {
    "mammoth": "https://i.ibb.co/PDqDKyC/mammoth.png",
    "chupacabra": "https://i.ibb.co/z5BZ0XY/chupacabra.png",
    "caesar": "https://i.ibb.co/cbDbwm4/ape.png",
    "dragon": "https://i.ibb.co/zWd8bbH/dragon.png",
    "kunjappan": "https://i.ibb.co/jv9sL69/kunj.png",
    "gryphon": "https://i.ibb.co/42m4PSq/gryphon.png",
    "devil": "https://i.ibb.co/pzrkb3X/devil.png",
    "werecat": "https://i.ibb.co/pr1pwLR/rakshas.png",
    "garuda": "https://i.ibb.co/m6QBQcQ/garuda.png",
    "yakshi": "https://i.ibb.co/SPTch0m/yak.png"
        }
stats = {
    "mammoth": {
        "str": 5,
        "agi": 2,
        "def": 3
    },
    "chupacabra": {
        "str": 3,
        "agi": 5,
        "def": 2
    },
    "caesar": {
        "str": 2,
        "agi": 6,
        "def": 2
    },
    "dragon": {
        "str": 4,
        "agi": 3,
        "def": 3
    },
    "kunjappan": {
        "str": 2.5,
        "agi": 2.5,
        "def": 5
    },
    "gryphon": {
        "str": 3.5,
        "agi": 3.5,
        "def": 3
    },
    "devil": {
        "str": 4,
        "agi": 4,
        "def": 2
    },
    "werecat": {
        "str": 2.5,
        "agi": 2.5,
        "def": 5
    },
    "garuda": {
        "str": 3,
        "agi": 3.5,
        "def": 3.5
    },
    "yakshi": {
        "str": 2.5,
        "agi": 5,
        "def": 2.5
    }
}


class Battle(commands.Cog):
    """NYTimes
    """

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def battle(self, ctx, p2: Member):
        p1 = ctx.author
        game = Embed(color=Color.green())
        beast = list(animals.keys())
        p1 = [p1, choice(beast)]
        hp = randrange(100, 300)
        b1 = [300, stats[p1[1]]]
        game.set_author(name=p1[1].title(), icon_url=animals[p1[1]])
        game.description = f"{p1[0].display_name} goes to battle with a {p1[1].title()}!"
        s = "**HP**: 300/300\n"
        for i in b1[1]:
            s += f"**{i.upper()}**: {b1[1][i]}\n"
        game.add_field(name="Stats", value=s)
        await ctx.send(embed=game)
        await sleep(2.5)
        p2 = [p2, choice(beast)]
        b2 = [300, stats[p2[1]]]
        game.set_author(name=p2[1].title(), icon_url=animals[p2[1]])
        game.description = f"{p2[0].display_name} goes to battle with a {p2[1].title()}!"
        s = "**HP**: 300/300\n"
        for i in b2[1]:
            s += f"**{i.upper()}**: {b2[1][i]}\n"
        game.set_field_at(index=0, name="Stats", value=s)
        await ctx.send(embed=game)
        await sleep(3)
        battle = Embed(color=Color.red())
        battle.description = "**Battle Start**!"
        msg = await ctx.send(embed=battle)
        await sleep(2)
        while b1[0] > 0 and b2[0] > 0:
            b1a = b1[1]['str']*10 - b2[1]['agi']*2.5 - b2[1]['def']*2.5 + randrange(10, 30)
            b2a = b2[1]['str']*10 - b1[1]['agi']*2.5 - b1[1]['def']*2.5 + randrange(10, 30)
            b1[0] -= b2a
            b2[0] -= b1a
            battle.set_author(name=p1[1].title(), icon_url=animals[p1[1]])
            log = f"{p1[0].display_name}'s {p1[1]} deals **{b1a}** damage!\n"
            log += f"HP **{b1[0]}**/**300**\n\n\n"
            log += f"{p2[0].display_name}'s {p2[1]} deals **{b2a}** damage!\n"
            log += f"HP **{b2[0]}**/**300**\n"
            battle.description = log
            battle.set_footer(text=p2[1].title(), icon_url=animals[p2[1]])
            await msg.edit(embed=battle)
            await sleep(3)
        result = Embed(color=Color.gold())
        await sleep(2)
        if b1[0] < 0 and b2[0] < 0:
            result.title = f"{ctx.author.display_name} and {p2.display_name}'s tied"
        else:
            win = p1 if b1[0] > b2[0] else p2
            result.title = f"🎉 {win[0].display_name} 🎉 won the battle! "
        result.set_thumbnail(url=animals[win[1]])
        await ctx.send(embed=result)


def setup(bot):
    bot.add_cog(Battle(bot))
