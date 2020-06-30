from discord.ext import commands
from aiohttp import ClientSession
from json import loads
from discord import Embed, Color
from random import choice


async def get(session: object, url: object) -> object:
    async with session.get(url) as response:
        return await response.text()


class HarryPotter(commands.Cog):
    """Harry Potter facts
    """

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='char', aliases=['character', 'ch'])
    async def character(self, ctx, *, name):
        name = name.title()
        base = "https://www.potterapi.com/v1/characters/?key=$2a$10$9eZjKMjumTqOfsZ7hk9EOO1u7GOY3jp7X/3deqi1DnwC0pexbJLrK"
        async with ClientSession() as session:
            data = await get(session, base)
        data = loads(data)
        ch = next((d for d in data if name == d['name']), None) or next((d for d in data if name in d['name']), None)
        hp = Embed()
        clr = None
        s2c = {
            "Gryffindor": 0xae0001,
            "Ravenclaw": 0x222f5b,
            "Slytherin": 0x2a623d,
            "Hufflepuff": 0xf0c75e,
            "Default": Color.dark_magenta()
        }
        hp.title = ch['name']
        if 'alias' in ch:
            hp.add_field(name="Alias", value=ch['alias'].title())
        if 'wand' in ch:
            hp.add_field(name="Wand", value=ch['wand'].title())
        if 'role' in ch:
            hp.add_field(name="Role", value=ch['role'].title())
        if 'house' in ch:
            hp.add_field(name="House", value=ch['house'].title())
            clr = s2c[ch['house']]
        if 'school' in ch:
            hp.add_field(name="School", value=ch['school'])
        if 'patronus' in ch:
            hp.add_field(name="Patronus", value=ch['patronus'].title())
        if 'boggart' in ch:
            hp.add_field(name="Boggart", value=ch['boggart'].title())

        hp.add_field(name="Blood Status", value=ch['bloodStatus'].title())
        hp.add_field(name="Species", value=ch['species'].title())
        de = "💀" if ch['deathEater'] else None
        if de:
            hp.add_field(name="Death Eater", value=de)
        de = "🧙‍♂️" if ch['dumbledoresArmy'] else None
        if de:
            hp.add_field(name="DA", value=de)
        de = "🐦" if ch['orderOfThePhoenix'] else None
        if de:
            hp.add_field(name="Order", value=de)
        de = "🤵" if ch['ministryOfMagic'] else None
        if de:
            hp.add_field(name="Ministry", value=de)

        base = "https://www.potterapi.com/v1/spells/?key=$2a$10$9eZjKMjumTqOfsZ7hk9EOO1u7GOY3jp7X/3deqi1DnwC0pexbJLrK"
        async with ClientSession() as session:
            data = await get(session, base)
        data = loads(data)

        data = choice(data)
        hp.set_footer(text=f"{data['spell']}: {data['effect']}")
        hp.color = clr or s2c['Default']
        return await ctx.send(embed=hp)


def setup(bot):
    bot.add_cog(HarryPotter(bot))
