from discord.ext import commands
from aiohttp import ClientSession
from json import loads
from discord import Embed, Color
from random import choice


async def get(session: object, url: object) -> object:
    async with session.get(url) as response:
        return await response.text()


class LOTR(commands.Cog):
    """LOTR facts
    """

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='lotr')
    async def lotr(self, ctx, *, name):
        name = name.title()
        base = "https://the-one-api.herokuapp.com/v1/character"
        auth = {"Authorization": "Bearer dRaxnLQ4pphf-B3knPlj"}
        async with ClientSession(headers=auth) as session:
            data = await session.get(url=base, headers=auth)
            data = await data.json()
        data = data['docs']
        ch = next((d for d in data if name in d['name']), None)
        if not ch:
            return
        lot = Embed(color=Color.green())
        lot.set_author(name="LOTR", icon_url="https://i.ibb.co/9v0H6V5/lotr.jpg")
        lot.title = ch['name']
        if ch['wikiUrl']:
            lot.url = ch['wikiUrl']
        lot.add_field(name="Race", value=ch['race'])
        if ch['gender'] != '':
            lot.add_field(name="Gender", value=ch['gender'])
        if ch['hair'] != '':
            lot.add_field(name="Hair", value=ch['hair'])
        if ch['birth'] != '':
            lot.add_field(name="Birth", value=ch['birth'])
        if ch['death'] != '':
            lot.add_field(name="Death", value=ch['death'])
        if ch['realm'] != '':
            lot.add_field(name="Realm", value=ch['realm'])
        if ch['spouse'] != '':
            lot.add_field(name="Spouse", value=ch['spouse'])
        if ch['height'] != '':
            lot.add_field(name="Height", value=ch['height'])
        return await ctx.send(embed=lot)


def setup(bot):
    bot.add_cog(LOTR(bot))
