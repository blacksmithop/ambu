from discord.ext import commands
from discord import Embed, Member, File
from asyncio import TimeoutError
from aiohttp import ClientSession
from io import BytesIO
from PIL import Image
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import lyricsgenius
from os import getenv as e
from datetime import datetime as dt


class Poll(commands.Cog):
    """Poll and other utilties
    """

    def __init__(self, bot):
        self.bot = bot
        self.sp = spotipy.Spotify(
            client_credentials_manager=SpotifyClientCredentials(client_id=e("SPOTIFY_CLIENT_ID"),
                                                                client_secret=e("SPOTIFY_CLIENT_SECRET")))
        self.lyric = lyricsgenius.Genius(client_access_token=e("genius"))

    async def u2b(self, url):
        async with ClientSession() as client_session:
            async with client_session.get(url) as response:
                return await response.read()

    @commands.command()
    async def poll(self, ctx):
        """
        Conduct a poll (interactive)
        ?poll
        """
        member = ctx.author
        member: Member
        maker = []
        await ctx.send("```What is the Question ❓```")
        em = ["🧪", "🧬", "🚀", "🖌️", "🧨"]

        def mcheck(m):
            return m.author == member

        try:
            msg = await self.bot.wait_for('message', timeout=20.0, check=mcheck)
            maker.append(msg.content)
        except TimeoutError:
            return await ctx.send("```Poll timed out ⏳```")

        await ctx.send("```How many options do you want?```")
        try:
            msg = await self.bot.wait_for('message', timeout=20.0, check=mcheck)
        except TimeoutError:
            return await ctx.send("```Poll timed out ⏳```")

        i = int(msg.content)
        if i > 20:
            return await ctx.send("```A maximum of 20 options for polls```")
        await ctx.send("```Enter your options ✔```")
        for i in range(i):
            try:
                await ctx.send(f"```{i + 1}) ```")
                msg = await self.bot.wait_for('message', timeout=20.0, check=mcheck)
                maker.append(msg.content)
                await msg.add_reaction("✅")
            except TimeoutError:
                return await ctx.send("```Poll timed out ⏳```")
        poller = Embed(color=0x5EE34)
        poller.title = maker[0]
        des = ''
        for j in range(1, len(maker)):
            des += f"```{em[j - 1]} {maker[j]}```\n"
        poller.description = des
        pr = await ctx.send(embed=poller)
        for j in range(i + 1):
            await pr.add_reaction(em[j])

        def reac_check(r, u):
            return pr.id == r.message.id and r.emoji in em

        eopt = {e: 0 for e in em}
        while True:
            try:
                reaction, user = await self.bot.wait_for('reaction_add', timeout=20.0, check=reac_check)
                e = str(reaction.emoji)
            except TimeoutError:
                await ctx.send("```Poll Finished ✅```")
                break
            if e in eopt.keys() and user != self.bot.user:
                eopt[e] += 1

        eopt = {k: v for k, v in sorted(eopt.items(), key=lambda item: item[1], reverse=True)}
        most = next(iter(eopt))
        loc = em.index(most)
        poller.title = "Results 🏆"
        poller.description = f"```Folks chose 📜\n{maker[loc + 1]}```"
        return await ctx.send(embed=poller)

    @commands.command()
    async def file(self, ctx, url: str):
        """
        Retrieve image from url (as png)
        ?file
        """
        image_bytes = await self.u2b(url)

        with Image.open(BytesIO(image_bytes)) as my_image:
            output_buffer = BytesIO()
            my_image.save(output_buffer, "png")  # or whatever format
            output_buffer.seek(0)

        await ctx.send(file=File(fp=output_buffer, filename=f"SPOILER_{url.split('/')[-1]}"))

    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def snap(self, ctx, url):
        """
        Retrieve snapshot of a website
        ?snap url
        """
        base = "https://image.thum.io/get/width/600/crop/600/"
        if 'https://' not in url:
            url = f"https://{url}"
        url = f"{base}{url}"

        image_bytes = await self.u2b(url)
        with Image.open(BytesIO(image_bytes)) as my_image:
            output_buffer = BytesIO()
            my_image.save(output_buffer, "png")
            output_buffer.seek(0)

        await ctx.send(file=File(fp=output_buffer, filename=f"SPOILER_webpage.png"))

    @commands.command()
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def artist(self, ctx, *, name: str):
        """
        Lookup an artist on spotify
        ?artist name
        """
        results = self.sp.search(q='artist:' + name, type='artist')
        items = results['artists']['items']
        if len(items) == 0:
            return
        artist = items[0]
        stat = Embed(color=0x1DB954)
        stat.title = artist['name']
        stat.url = artist['external_urls']['spotify']
        stat.set_image(url=artist['images'][0]['url'])

        follow = artist['followers']['total']
        if follow > 1000000:
            follow = int(follow // 1000000)
            follow = f"{follow}M"
        genre = ','.join(artist['genres'])
        stat.description = f'```Followes: {follow}\nGenre: {genre}```'
        stat.set_footer(icon_url="https://i.pinimg.com/564x/35/87/f8/3587f8e9df02e2990b93afb9cd6d2323.jpg",
                        text="Powered by Spotify")
        await ctx.send(embed=stat)

    @commands.command()
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def album(self, ctx, *, artist: str):
        """
        Lookup an album on spotify
        ?album name
        """
        results = self.sp.search(q='artist:' + artist, type='artist')
        items = results['artists']['items']
        if len(items) == 0:
            return
        artist = items[0]
        uri = artist['uri']
        top = self.sp.artist_top_tracks(uri)
        top = top['tracks'][:5]
        i = 0
        toggle = ["◀", "▶"]

        def tracker(i: int):
            return top[i]['album']['external_urls']['spotify']

        msg = await ctx.send(tracker(i=i))
        toggle = ["◀", "▶"]
        for em in toggle:
            await msg.add_reaction(em)

        def reac_check(r, u):
            return msg.id == r.message.id and u != self.bot.user and r.emoji in toggle

        while True:
            try:
                reaction, user = await self.bot.wait_for('reaction_add', timeout=15.0, check=reac_check)
                em = str(reaction.emoji)
                if user != self.bot.user:
                    await msg.remove_reaction(emoji=em, member=user)
            except TimeoutError:
                return
            if em == toggle[0]:
                if i == 0:
                    return
                else:
                    i -= 1
            elif em == toggle[1]:
                if i == 4:
                    return
                else:
                    i += 1
            await msg.edit(content=tracker(i=i))

    @commands.command()
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def song(self, ctx, *, song: str):
        """
        Lookup an song on spotify
        ?song name
        """
        song = self.sp.search(q=song, type='track', limit=1)
        await ctx.send(song['tracks']['items'][0]['external_urls']['spotify'])

    @commands.command(name='lines', aliases=['lyrics', 'l'])
    async def _lyrics(self, ctx: commands.Context, *, song: str):
        """
        Get song lyrics from Genius
        ?lyrics name
        """
        song = self.lyric.search_song(title=song)
        info = song
        song = song.lyrics.split('\n')
        song = [i for i in song if '[' not in i]
        n = 20
        song = [song[i * n:(i + 1) * n] for i in range((len(song) + n - 1) // n)]
        p = len(song)
        lyr = Embed(title=info.title, url=info.url)
        lyr.timestamp = dt.strptime(info.year, '%Y-%m-%d')
        lyr.set_thumbnail(url=info.song_art_image_url)
        i = 0
        lyr.set_footer(text=f"Page {i+1}/{p}")
        lyr.description = '\n'.join(song[i])
        toggle = ["◀", "▶"]
        msg = await ctx.send(embed=lyr)
        for e in toggle:
            await msg.add_reaction(e)

        def reac_check(r, u):
            return msg.id == r.message.id and u!=self.bot.user and r.emoji in toggle

        while True:
            try:
                reaction, user = await self.bot.wait_for('reaction_add', timeout=20.0, check=reac_check)
                em = str(reaction.emoji)
                if user!=self.bot.user:
                    await msg.remove_reaction(emoji=em, member=user)
            except TimeoutError:
                print("caught")
            if em == toggle[0]:
                if i == 0:
                    return
                else:
                    i -= 1
                    lyr.set_footer(text=f"Page {i + 1}/{p}")
                    lyr.description = '\n'.join(song[i])
                    await msg.edit(embed=lyr)
            elif em == toggle[1]:
                if i == p:
                    return
                else:
                    i += 1
                    lyr.set_footer(text=f"Page {i + 1}/{p}")
                    lyr.description = '\n'.join(song[i])
                    await msg.edit(embed=lyr)


def setup(bot):
    bot.add_cog(Poll(bot))
