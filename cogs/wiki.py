from discord.ext import commands
from discord import Embed, Color
from wikipediaapi import Wikipedia


class Wiki(commands.Cog):
    """Error handling.
    """

    def __init__(self, bot):
        self.bot = bot
        self.wiki = Wikipedia('en')

    @commands.command(name='wiki', aliases=['page'])
    async def page(self, ctx, *, search):
        result = self.wiki.page(search)
        if not result.exists():
            return await ctx.send(embed=Embed(
                title="Page not found ⛔",
                description=f"No page was found under the name `{search}`",
                color=Color.blurple()
            ))
        wiki = Embed(color=Color.dark_gold())
        wiki.title = result.title
        wiki.url = result.fullurl
        wiki.description = f'{result.text[0:500]}...'
        wiki.set_footer(text="Powered by Wikipedia",
                        icon_url="https://i.ibb.co/jyX08CD/wikipedia-PNG39.png")
        wiki.timestamp = ctx.message.created_at
        return await ctx.send(embed=wiki)


def setup(bot):
    bot.add_cog(Wiki(bot))
