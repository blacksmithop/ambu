from discord.ext import commands
from aiohttp import ClientSession
from json import loads
from discord import Embed, Color


async def get(session: object, url: object) -> object:
    async with session.get(url) as response:
        return await response.text()


class GameOfThrones(commands.Cog):
    """Game Of Thrones facts
    """

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='got', aliases=['gameofthrones'])
    async def gcharacter(self, ctx, *, name):
        name = name.title()
        name = '+'.join(name.split())
        base = f"https://www.anapioficeandfire.com/api/characters/?name={name}"
        async with ClientSession() as session:
            data = await get(session, base)
        data = loads(data)[0]
        got = Embed(color=Color.green())
        got.set_author(name=data['name'])
        got.set_thumbnail(url="https://i.ibb.co/r41nbDV/got.png")
        got.add_field(name="Gender", value=data['gender'])
        if data['culture'] != '':
            got.add_field(name="Culture", value=data['culture'])
        if data['born'] != '':
            got.add_field(name="Birth", value=data['born'])
        if data['died'] != '':
            got.add_field(name="Death", value=data['died'])
        if data['titles']:
            if len(data['titles']) == 1:
                title = data['titles'][0]
            else:
                title = '\n'.join(data['titles'])
            got.add_field(name="Titles", value=title)
        if data['aliases'][0] != "":
            alias = '\n'.join(data['aliases'])
            got.add_field(name="Aliases", value=f"```{alias}```")
        if data['playedBy'][0] != "":
            got.add_field(name="Played-By", value=data['playedBy'][0])
        return await ctx.send(embed=got)


def setup(bot):
    bot.add_cog(GameOfThrones(bot))
