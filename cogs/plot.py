from discord.ext import commands
from random import choice, randrange
from discord import Embed, Color, File
import matplotlib.pyplot as plt
from os import getcwd, chdir


def setup(bot):
    bot.add_cog(Plot(bot))


class Plot(commands.Cog):
    """Plot
    """

    def __init__(self, bot):
        self.bot = bot

    @commands.group()
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def odds(self, ctx):
        if ctx.invoked_subcommand is None:
            pass

    @odds.group(invoke_without_command=True)
    async def coin(self, ctx):
        def coinFlip():
            return choice([True, False])

        def simple_bettor(funds, initial_wager, wager_count):
            value = funds
            wager = initial_wager
            wX = []
            vY = []
            currentWager = 1

            while currentWager <= wager_count:
                if coinFlip():
                    value += wager
                    wX.append(currentWager)
                    vY.append(value)

                else:
                    value -= wager
                    wX.append(currentWager)
                    vY.append(value)

                currentWager += 1
            plt.plot(wX, vY)

        x = 0
        while x < 100:
            simple_bettor(100, 1, 100)
            x += 1
        clr = lambda: randrange(0, 255)
        colour = Color.from_rgb(clr(), clr(), clr())
        plt.ylabel('Account Value')
        plt.xlabel('Wager Count')
        chdir(f"{getcwd()}/cogs")
        plt.savefig('coin.png')
        file = File("coin.png", filename="coin.png")
        plot = Embed(title="Projection for Coin Flip", color=colour)
        plot.set_image(url="attachment://coin.png")
        await ctx.send(embed=plot, file=file)
