import redis
from json import loads, dumps


class BotConfig:

    def __init__(self):
        self.ses = redis.Redis(host="redis-17489.c11.us-east-1-2.ec2.cloud.redislabs.com",
                               port=17489,
                               password='5lM65RU4jr53isgWpvanzMCp5Ym2Tat0')

        self.guild_stats = {"prefix": None, "welcome": None, "verify": None, "logs": None,
                            "disabled": None, "muted": None, "testing": None, "member": None,
                            "invite": None, "leave": None}

    def ping(self):
        return self.ses.ping()

    def flush(self, id: int):
        return self.ses.flushdb() if id == 1234 else False

    def set(self, key: str, value: str, id: int, append: bool = False):
        guild = self.ses.get(id)
        if not guild:
            return False
        guild = loads(guild)
        if append:
            guild[key].append(value)
        else:
            guild[key] = value
        guild = dumps(guild)
        return self.ses.set(id, guild)

    def get(self, id: int, key: str = None):
        guild = self.ses.get(id)
        if not guild:
            return False
        guild = loads(guild)
        if not key:
            return guild
        return guild[key]

    def add(self, id: int):
        print(self.guild_stats)
        return self.ses.set(id, dumps(self.guild_stats))

    def remove(self, id: int):
        return self.ses.delete(id)

    def value(self, key: str, value=None):
        if value is None:
            return self.ses.get(key).decode("utf-8")
        return self.ses.set(key, value)


db = BotConfig()
