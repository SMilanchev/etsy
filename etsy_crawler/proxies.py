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


class NoMatchingProxiesError(Exception):
    pass


class NoAnyProxiesError(Exception):
    pass


def get_proxy(countries: list) -> Proxy | None:
    with open(DB_PATH) as f:
        proxies_raw: list[dict[str, str]] = json.load(f)['proxies']

    proxies = [Proxy(**proxy) for proxy in proxies_raw]
    if not proxies:
        raise NoAnyProxiesError('You DO NOT HAVE any proxies! Add proxies, or set use_proxy to False')
    if countries:
        proxies = list(filter(lambda x: x.country in countries, proxies))
        if not proxies:
            raise NoMatchingProxiesError('No proxies from selected countries! Change selected countries!')
    proxies_sorted_by_usage = sorted(proxies, key=lambda x: x.usage)
    if proxies_sorted_by_usage:
        proxy = proxies_sorted_by_usage[0]
        proxy.add_usage()
        return proxy


def save_proxy(proxy: Proxy):
    with open(DB_PATH) as f:
        proxies_raw: list[dict[str, str]] = json.load(f)['proxies']

    for i in range(len(proxies_raw)):
        current_proxy = proxies_raw[i]
        if current_proxy['username'] == proxy.username and current_proxy['password'] == proxy.password and\
                current_proxy['host'] == proxy.host and current_proxy['port'] == proxy.port:
            proxies_raw[i] = proxy.dict()
            with open(DB_PATH, 'w') as f:
                f.write(json.dumps({'proxies': proxies_raw}))


def delete_expiring_proxies():
    with open(DB_PATH) as f:
        proxies_raw: list[dict[str, str]] = json.load(f)['proxies']

    proxies = [Proxy(**proxy) for proxy in proxies_raw]
    proxies_to_save = []
    for proxy in proxies:
        current_dt = datetime.now()
        datetime_end = datetime.fromisoformat(proxy.end_date)
        remaining_seconds = int((datetime_end.astimezone().replace(tzinfo=None) - current_dt).total_seconds())
        if remaining_seconds > 60*60 * LEFT_HOURS_PROXY_TO_REMOVE:
            proxies_to_save.append(proxy)

    with open(DB_PATH, 'w') as f:
        f.write(json.dumps({'proxies': [p.dict() for p in proxies]}))
