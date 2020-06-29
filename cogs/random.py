from discord.ext import commands
from discord import Embed, Color
from aiohttp import ClientSession
from json import loads


async def get(session: object, url: object) -> object:
    async with session.get(url) as response:
        return await response.text()


class Random(commands.Cog):
    """Random data
    """

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def hero(self, ctx, *, name):
        stat = Embed(color=Color.red())
        base = f"https://www.superheroapi.com/api.php/3194171637307667/search/{name}"
        async with ClientSession() as session:
            data = await get(session, base)
        data = loads(data)
        if data['response'] != 'success':
            return await ctx.send("Hero not found")
        data = data['results'][0]
        stat.set_author(name=f"{data['biography']['full-name']}/{data['name']}")
        stat.set_thumbnail(url=data['image']['url'])
        power = data['powerstats']
        s = f"""INT 🧠: {power['intelligence']}\nSTR 💪: {power['strength']}\nAGI 🏃: {power['speed']}\nEND 🗻: {power['durability']}\nPOW ☢: {power['power']}\nCombat 🗡: {power['combat']}‍"""
        stat.add_field(name="Stats", value=f"```{s}```")
        g2e = {
            "Male": "♂️",
            "Female": "♀️"
        }
        about = data['appearance']
        a = f"""Gender: {g2e[about['gender']] or g2e['Male']}\nRace: {about['race']}\nHeight: {about['height'][0]}\nWeight: {about['weight'][0]}\nWork: {data['work']['occupation']}\nBase: {data['work']['base']}"""
        stat.add_field(name="About", value=f"```{a}```")
        stat.set_footer(text=f"Alignment: {data['biography']['alignment']}")
        return await ctx.send(embed=stat)

    @commands.command()
    async def drink(self, ctx):
        tail = Embed(color=Color.gold())
        base = "https://www.thecocktaildb.com/api/json/v1/1/random.php"
        async with ClientSession() as session:
            data = await get(session, base)
        data = loads(data)
        data = data['drinks'][0]
        tail.set_author(name=data['strDrink'])
        tail.set_thumbnail(url=data['strDrinkThumb'])
        tail.add_field(name="Alcoholic 🍻", value=data['strAlcoholic'])
        tail.add_field(name="Category", value=data['strCategory'])
        ingr = ""
        for i in range(1, 17):
            item = data[f'strIngredient{i}']
            if item is None:
                break
            ingr += f'{item}\n'
        tail.add_field(name="Ingridients", value=f'```{ingr}```', inline=False)
        tail.add_field(name="Instructions", value=f"```{data['strInstructions']}```", inline=False)
        return await ctx.send(embed=tail)

    @commands.command(name='so', aliases=['stack', 'stackoverflow'])
    async def stack(self, ctx, *, query):
        so = Embed(color=Color.dark_blue())
        query = '+'.join(query.split())
        base = f"https://api.stackexchange.com/2.2/search/advanced?pagesize=1&order=desc&sort=votes&q={query}&site=stackoverflow"
        async with ClientSession() as session:
            data = await get(session, base)
        data = loads(data)
        so.set_thumbnail(url="https://i.ibb.co/X4DWhts/so.png")
        data = data['items'][0]
        so.set_footer(text=f"Tags: {','.join(data['tags'])}")
        so.set_author(name=data['title'], url=data['link'], icon_url=data['owner']['profile_image'])
        so.description = f"Score: {data['score']}\nAnswers: {data['answer_count']}\nBy [{data['owner']['display_name']}]({data['owner']['link']})"
        return await ctx.send(embed=so)

    @commands.command(name='word', aliases=['dict', 'dictionary'])
    async def word(self, ctx, *, query):
        query = '+'.join(query.split())
        word = Embed(color=Color.green())
        head = {"Authorization": "Token f3159a463cde0f06b3fcb2433bcccc79f549b753"}
        base = f"https://owlbot.info/api/v4/dictionary/{query}"
        async with ClientSession(headers=head) as session:
            data = await session.get(url=base, headers=head)
            data = await data.json()
        mean = data['definitions'][0]
        word.set_author(name=f"{data['word']} ({data['pronunciation']})")
        if mean['image_url'] is not None:
            word.set_thumbnail(url=mean['image_url'])
        word.description = f"({mean['type']}) {mean['definition']}"
        return await ctx.send(embed=word)

    @commands.command(name='joke')
    async def joke(self, ctx):
        base = "https://sv443.net/jokeapi/v2/joke/Any?blacklistFlags=nsfw,racist,sexist&type=twopart"
        async with ClientSession() as session:
            data = await get(session, base)
        data = loads(data)
        j = Embed(color=0xFFA500)
        j.set_footer(text=data['category'])
        j.description = f"```{data['setup']}\n\n{data['delivery']}```"
        return await ctx.send(embed=j)


def setup(bot):
    bot.add_cog(Random(bot))
