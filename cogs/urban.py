from discord.ext import commands
from discord import Embed
from aiohttp import ClientSession
from json import loads


async def get(session: object, url: object) -> object:
    async with session.get(url) as response:
        return await response.text()


async def urban(data):
    data = loads(data)
    if len(data['list']) == 0:
        return False
    data = data['list'][0]
    udef = Embed()
    udef.color = 0x114ee8
    udef.title = data['word']
    udef.description = f"**Definition:**\n\n{data['definition']}\n\n**Example:**\n\n{data['example']}"
    udef.url = data['permalink']
    udef.set_footer(text=f"{data['thumbs_up']} 👍 {data['thumbs_down']} 👎 by {data['author']}",
                    icon_url="https://i.ibb.co/3fsGdvp/unnamed.png")
    return udef


class Urban(commands.Cog):
    """Urban Dictionary
    """

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='ud', aliases=['define', 'urban'])
    async def _urbandict(self, ctx, *, term):
        """
        Get Urban Dictionary definitions
        ?ud word
        """
        term = term.replace(" ", "+")
        url = f"http://api.urbandictionary.com/v0/define?term={term}"
        async with ClientSession() as session:
            data = await get(session, url)
        data = await urban(data)
        if data is False:
            return await ctx.send(f'Could not find UD entry for {term}')
        return await ctx.send(embed=data)


def setup(bot):
    bot.add_cog(Urban(bot))
