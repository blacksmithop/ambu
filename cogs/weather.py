from discord.ext import commands
from discord import Embed, Color
from aiohttp import ClientSession
from json import loads
from darksky.api import DarkSky
from datetime import datetime
from darksky.types import languages, units, weather

KEY = '062938f70cd12c05b1c985bb70761e8f'
darksky = DarkSky(KEY)


async def get(session: object, url: object) -> object:
    async with session.get(url) as response:
        return await response.text()


class Weather(commands.Cog):
    """Weather data
    """

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='weather', aliases=['climate'])
    async def weather(self, ctx, *, address):
        address = '+'.join(address.split())
        base = f"https://api.opencagedata.com/geocode/v1/json?q={address}&key=54939abc79ce4650a77f3beca24335d2"
        async with ClientSession() as session:
            data = await get(session, base)
        data = loads(data)
        try:
            data = data['results'][0]
            data = data['bounds']['northeast']
            latitude = data['lat']
            longitude = data['lng']
        except:
            latitude = 11.8745
            longitude = 75.3704
        forecast = darksky.get_time_machine_forecast(latitude=latitude, longitude=longitude,
                                                     extend=False,  # default `False`
                                                     lang=languages.ENGLISH,  # default `ENGLISH`
                                                     values_units=units.AUTO,  # default `auto`
                                                     exclude=[weather.MINUTELY, weather.ALERTS],  # default `[]`,
                                                     timezone='UTC',
                                                     # default None - will be set by DarkSky API automatically
                                                     time=datetime.now()
                                                     )
        wea = Embed(color=Color.blue())
        wea.set_author(name=forecast.currently.summary)
        wea.add_field(name="Temperature", value=forecast.currently.temperature)
        w2i = {
            "default": "https://i.ibb.co/sCzzWJx/weather.jpg",
            "clear-day": "https://i.ibb.co/yRFYXRG/sun.jpg",
            "cloudy": "https://i.ibb.co/TTQZBNF/cloud.jpg",
            "rain": "https://i.ibb.co/THm0kGD/rain.png"
        }
        if forecast.currently.icon in w2i:
            icon = w2i[forecast.currently.icon]
        else:
            icon = w2i['default']
        wea.set_thumbnail(url=icon)
        wea.add_field(name="Humidity", value=forecast.currently.humidity)
        wea.add_field(name="Pressure", value=forecast.currently.pressure)
        wea.add_field(name="Wind Speed", value=forecast.currently.wind_speed)
        wea.add_field(name="Cloud Cover", value=forecast.currently.cloud_cover)
        wea.add_field(name="Dew Point", value=forecast.currently.dew_point)
        wea.add_field(name="UV Index", value=forecast.currently.uv_index)
        wea.add_field(name="Precipitation", value=forecast.currently.precip_intensity)
        wea.add_field(name="Visibility", value=forecast.currently.visibility)
        return await ctx.send(embed=wea)


def setup(bot):
    bot.add_cog(Weather(bot))
