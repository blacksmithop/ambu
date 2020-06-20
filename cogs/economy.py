from discord.ext import commands
from discord import Embed, Member, Status, Color
import db
from discord.utils import get
from aiohttp import ClientSession
from ast import literal_eval as l
from random import shuffle, randrange
from asyncio import TimeoutError


async def fetch(session: object, url: object) -> object:
    async with session.get(url) as response:
        return await response.text()


class Economy(commands.Cog):
    """Error handling.
    """

    def __init__(self, bot):
        self.bot = bot
        self.db = db.BotConfig()
        self.guild = self.bot.get_guild(self.db.fetch(name="emote"))
        self.on = get(self.guild.emojis, name="online")
        self.off = get(self.guild.emojis, name="offline")
        self.idle = get(self.guild.emojis, name="idle")
        self.dnd = get(self.guild.emojis, name="dnd")

    @commands.command(name='balance', aliases=['bank', 'bal'])
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def balance(self, ctx, member: Member = None):
        """
        Shows user balance
        ?bal
        """
        if member is None:
            member = ctx.author
        user = Embed(color=0x857272)
        user.set_author(name=member.display_name, icon_url=member.avatar_url)
        bal = self.db.getuser(uid=member.id)
        user.description = f"```Balance: {bal} 🥥```"
        user.timestamp = ctx.message.created_at
        await ctx.send(embed=user)

    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def user(self, ctx, member: Member = None):
        """
        Shows user balance information
        ?user member
        """
        if member is None:
            member = ctx.author

        e2s = {
            Status.online: self.on,
            Status.offline: self.off,
            Status.idle: self.idle,
            Status.dnd: self.dnd

        }

        user = Embed(color=member.color)
        user.set_author(name=member)
        user.set_thumbnail(url=member.avatar_url)
        user.timestamp = ctx.message.created_at
        user.add_field(name="Status", value=e2s[member.status], inline=True)
        user.add_field(name="Joined", value=member.joined_at.strftime("%d-%m-%Y"), inline=True)
        user.add_field(name="Created", value=member.created_at.strftime("%d-%m-%Y"), inline=True)
        user.add_field(name="Nickname", value=member.display_name, inline=True)
        mob = "📱" if member.is_on_mobile() else "📵"
        user.add_field(name="Mobile", value=mob, inline=True)
        roles = member.roles
        user.add_field(name="Roles", value=', '.join([role.mention for role in roles]), inline=False)
        if member.status is Status.offline:
            return await ctx.send(embed=user)
        act = member.activities
        try:
            if act[0]:
                try:
                    user.add_field(name="Activity 🍞", value=f"{act[0].emoji.name or ''} {act[0].name}", inline=True)
                except:
                    user.add_field(name="Spotify 🎶", value=f"{act[0].title} by {act[0].artist}", inline=True)
        except:
            pass
        try:
            if act[1]:
                try:
                    user.add_field(name="Spotify 🎶", value=f"{act[1].title} by {act[1].artist}", inline=True)
                except:
                    try:
                        user.add_field(name="Custom 😎", value=f"{act[1].name}, {act[1].details}", inline=True)
                        if act[2]:
                            try:
                                user.add_field(name="Spotify 🎶", value=f"{act[2].title} by {act[2].artist}",
                                               inline=True)
                            except:
                                pass
                    except:
                        pass
        except:
            pass
        await ctx.send(embed=user)

    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def trivia(self, ctx):
        url = "https://opentdb.com/api.php?amount=1&difficulty=medium&type=multiple"
        clr = lambda: randrange(0, 255)
        colour = Color.from_rgb(clr(), clr(), clr())
        async with ClientSession() as session:
            url = await fetch(session, url)
        url = l(url)
        quest = Embed(color=colour)
        url = url['results'][0]
        quest.title = f"""Q) **{url['question'].replace('&quot;', "'").replace('&#039;', "'")}**"""
        quest.set_author(name=url['category'], icon_url="https://i.ibb.co/FztStPF/trivia-Icon.png",
                         url="https://opentdb.com/")
        correct = url['correct_answer']
        answers = url['incorrect_answers']
        answers.append(correct)
        shuffle(answers)
        quest.description = f"""A. {answers[0]}\n
                            B. {answers[1]}\n
                            C. {answers[2]}\n
                            D. {answers[3]}
                            """
        mcq = await ctx.send(embed=quest)
        reacts = ['🇦', '🇧', '🇨', '🇩']

        r2a = {
            '🇦': answers[0],
            '🇧': answers[1],
            '🇨': answers[2],
            '🇩': answers[3]
        }
        ans = {"R": {*()}, "W": {*()}}
        for react in reacts:
            await mcq.add_reaction(react)

        while True:
            try:
                reaction, user = await self.bot.wait_for('reaction_add', timeout=20.0)
                e = str(reaction.emoji)
            except TimeoutError:
                break
            if user != self.bot.user and reaction.message.id == mcq.id:
                if r2a[e] == correct:
                    ans["R"].add(user.id)
                else:
                    ans["W"].add(user.id)

        des = ""
        for right in ans["R"]:
            if right not in ans["W"]:
                des += f"<@{right}> won 10 🥥\n"
        if des != "":
            des = f"```Correct answer was {correct}```\n{des}"
            await ctx.send(embed=Embed(description=des, color=colour))
        else:
            des = f"```Correct answer was {correct}```\nNo winners 😢"
            await ctx.send(embed=Embed(description=des, color=colour))


def setup(bot):
    bot.add_cog(Economy(bot))
