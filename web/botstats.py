from aiohttp import web, ClientSession
from os import getenv as e
import aiohttp_jinja2
import jinja2
routes = web.RouteTableDef()
auth = {'Authorization': f"Bot {e('token')}"}


async def startup():
    base = f"https://discord.com/api/users/199129403458977792"
    async with ClientSession(headers=auth) as session:
        resp = await session.get(url=base, headers=auth)
        gid = await resp.json()
    av, id = gid['avatar'], gid['id']
    return f"https://cdn.discordapp.com/avatars/{id}/{av}.png"


@routes.get('/guild/{guild}')
async def guild(request):
    gid = request.match_info['guild']
    base = f"https://discord.com/api/guilds/{gid}?with_counts=True"
    async with ClientSession(headers=auth) as session:
        resp = await session.get(url=base, headers=auth)
        gid = await resp.json()
    keep = ['id', 'name', 'owner_id', 'region', 'approximate_member_count']
    gid = {k: gid[k] for k in keep}
    return web.json_response(gid)

@routes.get('/')
async def index(request):
    av = await startup()
    return aiohttp_jinja2.render_template('index.html', request, context=None)


if __name__ == '__main__':
    app = web.Application()
    app.add_routes(routes)
    aiohttp_jinja2.setup(app, loader=jinja2.FileSystemLoader('./'))
    web.run_app(app, port=e('PORT'))
