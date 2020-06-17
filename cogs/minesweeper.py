import random
import numpy as np
from discord.ext import commands
from discord import Embed


class Board:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        number_of_mines = (width - 1) * (height - 1)
        self.number_of_mines = number_of_mines
        board = np.array([[0 for i in range(width + 2)] for j in range(height + 2)], dtype=str)
        self.board = board
        for i in range(number_of_mines):
            # generate random co-ords for bombs
            while True:
                x_pos, y_pos = random.randint(1, width), random.randint(1, height)
                if self.board[y_pos, x_pos] != 'b':
                    self.board[y_pos, x_pos] = 'b'
                    break

        # iterate over each square of the board
        for y_pos in range(0, height + 2):
            for x_pos in range(0, width + 2):
                # if the square in question is a bomb then skip it
                if self.board[y_pos, x_pos] == 'b':
                    continue
                adj_squares = self.board[max((y_pos - 1), 0):min(height + 2, y_pos + 2),
                              max((x_pos - 1), 0):min(width + 2, x_pos + 2)]
                count = 0
                for square in np.nditer(adj_squares):
                    if square == 'b':
                        count += 1

                self.board[y_pos, x_pos] = str(count)


class Minesweeper(commands.Cog):
    """Error handling.
    """

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='ms')
    async def _minesweeper(self, ctx):
        """
        Play Minesweeper
        ?ms
        """
        game = Embed(color=0xF10D0D)
        game.title = "Minesweeper 💣"
        board = ""
        test = Board(4, 4)
        for b in test.board:
            b = ['||💥||' if x == 'b' else f'||-{x}-||' for x in b]
            b.append('\n')
            board += ''.join(b)
        game.description = board
        await ctx.send(embed=game)


def setup(bot):
    bot.add_cog(Minesweeper(bot))


