from discord.ext import commands
from discord import Embed, Color
from itertools import cycle
from asyncio import TimeoutError


def view_board(board):
    view = '\n─────────────────\n'
    for i in range(3):
        for j in range(3):
            view += f"| {board[i][j]} |"
        view += '\n─────────────────\n'
    return f"```{view}```"


def win(board):
    def all_same(l):
        if l.count(l[0]) == len(l) and l[0] != 0:
            return True
        else:
            return False

    # horizontal
    for row in board:
        print(row)
        if all_same(row):
            print(f"Player {row[0]} is the winner horizontally!")
            return True

    # vertical
    for col in range(len(board[0])):
        check = []
        for row in board:
            check.append(row[col])
        if all_same(check):
            print(f"Player {check[0]} is the winner vertically!")
            return True

    # / diagonal
    diags = []
    for idx, reverse_idx in enumerate(reversed(range(len(board)))):
        diags.append(board[idx][reverse_idx])

    if all_same(diags):
        print(f"Player {diags[0]} has won Diagonally (/)")
        return True

    # \ diagonal
    diags = []
    for ix in range(len(board)):
        diags.append(board[ix][ix])

    if all_same(diags):
        print(f"Player {diags[0]} has won Diagonally (\\)")
        return True

    return False


def gboard(board, player=0, row=0, column=0, just_display=False):
    try:
        if board[row][column] != 0:
            return False

        if not just_display:
            board[row][column] = player
        return board
    except IndexError:
        return False
    except Exception:
        return False


class TicTacToe(commands.Cog):
    """Error handling.
    """

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='tc')
    async def tictac(self, ctx):
        board = [[0] * 3 for _ in range(3)]
        game = Embed(color=Color.green())
        game.timestamp = ctx.message.created_at
        game.set_author(name="TicTacToe ❌ ⭕", icon_url="https://i.ibb.co/bP3wRgY/download.png")
        members = set()
        game.set_footer(text=f"React with ✅ to join game")
        msg = await ctx.send(embed=game)
        await msg.add_reaction('✅')

        def check(r, u):
            return u != self.bot.user and r.emoji == "✅"

        while True:
            try:
                await self.bot.wait_for(event="reaction_add", timeout=15, check=check)
            except TimeoutError:
                break
        msg = await ctx.channel.fetch_message(id=msg.id)
        for reaction in msg.reactions:
            async for user in reaction.users():
                members.add(user)
        members.remove(self.bot.user)
        members = list(members)[:2]
        play = True
        while play:
            gwon = False
            player_cycle = cycle(members)
            gboard(board, just_display=True)
            while not gwon:
                current_player = next(player_cycle)
                played = False
                while not played:
                    game.description = view_board(board)
                    game.set_footer(text=f"{current_player}'s turn")
                    await ctx.send(embed=game)

                    def hcheck(m):
                        return m.author != self.bot.user and m.author == current_player

                    try:
                        msg = await self.bot.wait_for('message', timeout=20.0, check=hcheck)
                    except TimeoutError:
                        return
                    rc = list(msg.content)
                    rc = [int(i) - 1 for i in rc]
                    print(rc)
                    mem = list(members)
                    m2e = {
                        mem[0]: "❌",
                        mem[1]: "⭕"
                    }
                    played = gboard(board, player=m2e[current_player], row=rc[0], column=rc[1])

                if win(board):
                    game.description = view_board(board)
                    await ctx.send(embed=game)
                    return await ctx.send(embed=Embed(
                        title="🎇 Game Over 🎆!",
                        description=f"Player {current_player} has won!",
                        color=Color.dark_gold(),
                        timestamp=ctx.message.created_at
                    ))


def setup(bot):
    bot.add_cog(TicTacToe(bot))
