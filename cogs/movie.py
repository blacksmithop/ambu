from discord.ext import commands
from discord import Embed
from os import getenv as e
from aiohttp import ClientSession
from json import loads


async def get(session: object, url: object) -> object:
    async with session.get(url) as response:
        return await response.text()


class Movie(commands.Cog):
    """Lookup movies/Series
    """

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="movie", aliases=['mov', 'm'])
    async def _movie(self, ctx, *, title):
        """Search for a Movie/Series
        ?mov name
        """
        async with ClientSession() as session:
            url = f"http://www.omdbapi.com/?t={'+'.join(title.split())}&apikey={e('omdb')}"
            url = await get(session, url)
            url = loads(url)
        movie = Embed(color=0x8311f5)
        await ctx.send(embed=Embed(title =f"**{url['Title']}** ({url['Rated']})",
                                   description=f"```\n{url['Runtime']}\n{url['imdbRating']}```",
                                   color=0x7309de
                                   ).set_image(url=url["Poster"]))

        movie.title = "Stats 🎬"
        movie.add_field(name="Plot", value=f"```css\n\"{url['Plot']}\"```", inline=False)
        movie.add_field(name="Directed by", value=f"```fix\n{url['Director']}```", inline=True)
        movie.add_field(name="Cast", value=f"```diff\n- {url['Actors']}```", inline=True)
        movie.add_field(name="Awards", value=f"```bash\n\"{url['Awards']}\"```", inline=True)
        movie.set_footer(text=f"Release: {url['Released']}")
        await ctx.send(embed=movie)


def setup(bot):
    bot.add_cog(Movie(bot))
