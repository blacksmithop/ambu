from discord.ext import commands
from deep_translator import GoogleTranslator
from discord import Embed


def setup(bot):
    bot.add_cog(Translate(bot))

    # translate to Malayalam


class Translate(commands.Cog):
    """
    Translate text
    """

    def __init__(self, bot):
        self.bot = bot
        self.translator = GoogleTranslator(source='auto', target='ml')

    @commands.command(name='m',
                      help='Translate any language to Malayalam',
                      usage='.km How are you?')
    @commands.cooldown(1, 3, commands.BucketType.user)
    @commands.bot_has_permissions(embed_links=True)
    async def _malayalam(self, ctx, *, text: str):
        if len(text.split()) > 100:
            return await ctx.send("Text cannot have more than 100 words")

        mal_text = self.translator.translate(text)
        trans = Embed(color=0x50C878)
        trans.timestamp = ctx.message.created_at
        trans.title = "മലയാള വിവർത്തനം"
        trans.url = "https://translate.google.com/"
        trans.description = f'**Query:** ```{text}```\n**TL:** ```{mal_text}```'
        await ctx.send(embed=trans)
