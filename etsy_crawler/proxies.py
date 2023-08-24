import json
from datetime import datetime

from pydantic import BaseModel

from settings import DB_PATH, LEFT_HOURS_PROXY_TO_REMOVE, PROXY_DATETIME_FORMAT


class Proxy(BaseModel):
    username: str
    password: str
    host: str
    port: str
    country: str
    version: str
    usage: int = 0
    last_usage: str | None = None
    end_date: str

    @property
    def uri(self) -> str:
        return f'http://{self.username}:{self.password}@{self.host}:{self.port}'

    def add_usage(self):
        self.usage += 1
        self.last_usage = datetime.now().strftime(PROXY_DATETIME_FORMAT)

    def get_proxy_db_index(self, proxies_db: list[dict]):
        for i in range(len(proxies_db)):
            current_proxy = proxies_db[i]
            if self.username == current_proxy['username'] and \
               self.password == current_proxy['password'] and \
               self.host == current_proxy['host'] and \
               self.port == current_proxy['port']:
                return i

    def save(self):
        with open(DB_PATH) as f:
            proxies_raw: list[dict[str, str]] = json.load(f)['proxies']

        proxy_db_index = self.get_proxy_db_index(proxies_db=proxies_raw)
        proxies_raw[proxy_db_index] = self.dict()
        with open(DB_PATH, 'w') as f:
            f.write(json.dumps({'proxies': proxies_raw}))


class NoMatchingProxiesError(Exception):
    """Raised when there are proxies in the proxies_db.json,
    but none of them matches the criterias requested by user."""
    pass


class NoAnyProxiesError(Exception):
    """Raised when there are no proxies is the proxies_db.json,
    but the user has requested the program to use proxy."""
    pass


def get_proxy(countries: list, versions: list) -> Proxy | None:
    with open(DB_PATH) as f:
        proxies_raw: list[dict[str, str]] = json.load(f)['proxies']

    proxies = [Proxy(**proxy) for proxy in proxies_raw]
    if not proxies:
        raise NoAnyProxiesError('You DO NOT HAVE any proxies! Add proxies, or set use_proxy to False')

    if countries:
        proxies = list(filter(lambda proxy: proxy.country in countries, proxies))
        if not proxies:
            raise NoMatchingProxiesError('No proxies from selected countries! Change selected countries!')

    if versions:
        proxies = list(filter(lambda proxy: proxy.version in versions, proxies))
        if not proxies:
            raise NoMatchingProxiesError('No proxies from selected versions! Change selected versions!')

    proxies_sorted_by_usage = sorted(proxies, key=lambda x: x.usage)
    if proxies_sorted_by_usage:
        proxy = proxies_sorted_by_usage[0]
        proxy.add_usage()
        proxy.save()
        return proxy


def delete_expiring_proxies():
    with open(DB_PATH) as f:
        proxies_raw: list[dict[str, str]] = json.load(f)['proxies']

    proxies = [Proxy(**proxy) for proxy in proxies_raw]
    proxies_to_save = []
    for proxy in proxies:
        current_dt = datetime.now()
        datetime_end = datetime.fromisoformat(proxy.end_date)
        remaining_seconds = int((datetime_end.astimezone().replace(tzinfo=None) - current_dt).total_seconds())
        if remaining_seconds > 60 * 60 * LEFT_HOURS_PROXY_TO_REMOVE:
            proxies_to_save.append(proxy)

    with open(DB_PATH, 'w') as f:
        f.write(json.dumps({'proxies': [p.dict() for p in proxies_to_save]}))
