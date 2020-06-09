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
            "welcome": {
                "channel": none,
                "message": none,
                "information": none
            },
            "leave": {
                "channel": none,
                "message": none
            },
            "roles": {
                "self": none,
                "member": none,
                "admin": none,
                "muted": none,
                "testing": none
            },
            "logs": {
                "channel": none,
                "delete": none,
                "edit": none,
                "roleadd": none,
                "roleremove": none,
                "invitecreate": none
            },
            "verification": {
                "verify": none,
                "message": none,
                "joinrole": none
            },
            "prefix": none,
            "invitefilter": none,
            "bans": none,
            "maxwarns": none,

            "testing": {
                "channel": none,
                "members": none
            },
            "cussfilter": none,
            "spamfilter": none
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

    def getparam(self, key: [] or str, id: int):
        if not self.r.exists(id):
            return
        guild = self.r.get(id)
        if len(key) == 2:
            guild = l(guild)
            guild = guild[key[0]][key[1]]
            guild = l(guild)
            return guild if guild!=d(None) else None

        else:
            guild = l(guild)[key[0]]
            if type(guild) is dict:
                return guild
            if l(guild) == d(None):
                guild = None
            else:
                guild = l(guild)
        return guild

    def setparam(self, key: [], value, sid: int):
        if not self.r.exists(sid):
            return
        guild = self.r.get(sid)
        guild = l(guild)
        if len(key) > 1:
            guild[key[0]][key[1]] = value
        else:
            guild[key[0]] = value
        return self.r.set(id, d(guild))

    def fetch(self, name: str):
        em = self.r.get(name)
        return l(em)



