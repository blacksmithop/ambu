from discord.ext import commands
from discord import Embed
from akinator.async_aki import Akinator as Aki
from asyncio import TimeoutError


def setup(bot):
    bot.add_cog(Akinator(bot))


class Akinator(commands.Cog):
    """
    Play a game of Akinator
    """

    def __init__(self, bot):
        self.bot = bot
        self.aki = Aki()

    @commands.command()
    @commands.max_concurrency(1, commands.BucketType.guild)
    async def aki(self, ctx):
        asker = ctx.author
        ques = Embed(color=asker.color)
        ques.set_author(name=asker, icon_url=asker.avatar_url)
        ques.description = "Yes, No, I Don't know, Probably, Probably not"
        ques.timestamp = ctx.message.created_at

        print(f'Starting akinator game with {asker.display_name}')
        # First question
        a = await self.aki.start_game()

        def auth_check(message):
            if message.author == asker:
                if message.content.lower() in ['yes', 'no', 'i dont know',
                                       'i don\'t know', 'probably',
                                       'probably not', 'end']:
                    return True

        ques.title = f"**{a}**"
        while self.aki.progression <= 80:
            print(self.aki.progression)
            ques.set_footer(text=f'{self.aki.step}')

            await ctx.send(embed=ques)
            try:
                ans = await self.bot.wait_for('message', check=auth_check, timeout=40)
            except TimeoutError:
                return await ctx.send("You took too long to answer, game ended")
            if ans.content.lower() == 'end':
                return await ctx.send("You have ended this round")
            a = await self.aki.answer(ans.content.lower())
            print(a)
            ques.title = f"**{a}**"
            ques.timestamp = ans.created_at
        await self.aki.win()
        guess = self.aki.first_guess
        ques.title = "Was your character...."
        ques.description = f"**{guess['name']}**\n{guess['description']}"
        await ctx.send(embed=ques)
