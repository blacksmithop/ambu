import redis
from os import getenv as e
from pickle import loads as l, dumps as d


class BotConfig:

    def __init__(self):
        self.r = redis.Redis(host=e("host"),
                             port=17489,
                             password=e("pwd"))
        none = d(None)
        self.guild = {
            "prefix": none,

            "channels": {
                "welcome": {
                    "channel": none,
                    "message": none,
                    "information": none
                },
                "leave": {
                    "channel": none,
                    "message": none
                },
                "logs": {
                    "channel": none,
                    "delete": none,
                    "edit": none,
                    "role": none,
                    "invite": none
                },
                "testing": {
                    "channel": none
                }
            },

            "roles": {
                "self": none,
                "member": none,
                "mod": none,
                "muted": none,
                "dev": none
            },

            "verify": {
                "channel": none,
                "message": none,
                "role": none
            },

            "filters": {
                "swear": none,
                "spam": none,
                "invite": none
            }
        }

    def addguild(self, id: int):
        return self.r.set(id, d(self.guild))

    def removeguild(self, id: int):
        return self.r.delete(id, self.guild)

    def getguild(self, id: int):
        if not self.r.exists(id):
            return

        guild = self.r.get(id)
        guild = l(guild)
        return guild

    def str2bool(self, flag: str):
        return True if flag is 'True' else False

    def getchannel(self, id: int, channel: str = None):
        guild = self.getguild(id=id)
        if guild:
            if channel is None:
                return guild['channels']

            g = guild['channels'][channel]
            g = {k: l(g.get(k)) for k in g.keys()}
            return g

    def setchannel(self, id: int, key: str, v1: str, v2: str):
        guild = self.getguild(id=id)
        if guild:
            g = guild['channels']
            if key not in g.keys():
                return False
            g = g[key]
            g[v1] = d(v2)
            guild['channels'][key] = g
            return self.r.set(id, d(guild))

    def getrole(self, id: int, role: str = None):
        guild = self.getguild(id=id)
        if guild:
            g = guild['roles']
            g = {k: l(g.get(k)) for k in g.keys()}
            if role:
                return g[role]
            return g

    def setrole(self, id: int, key: str, value: str):
        guild = self.getguild(id=id)
        if guild:
            g = guild['roles']
            if key not in g.keys():
                return False
            g[key] = d(value)
            guild['roles'] = g
            return self.r.set(id, d(guild))

    def getfilter(self, id: int, filter: str = None):
        guild = self.getguild(id=id)
        if guild:
            g = guild['filters']
            g = {k: l(g.get(k)) for k in g.keys()}

            for k in list(g.keys())[1:]:
                g[k] = self.str2bool(flag=g[k])
            if filter:
                return g[filter]
            return g

    def setfilter(self, id: int, key: str, value: str):
        guild = self.getguild(id=id)
        if guild:
            g = guild['filters']
            if key not in g.keys():
                return False
            g[key] = d(value)
            guild['filters'] = g
            return self.r.set(id, d(guild))

    def getprefix(self, id: int):
        guild = self.getguild(id=id)
        if guild:
            return l(guild['prefix'])

    def setprefix(self, id: int, new_prefix: str):
        guild = self.getguild(id=id)
        if guild and new_prefix:
            guild['prefix'] = d(new_prefix)
            return self.r.set(id, d(guild))

    def fetch(self, name: str):
        em = self.r.get(name)
        return l(em)
