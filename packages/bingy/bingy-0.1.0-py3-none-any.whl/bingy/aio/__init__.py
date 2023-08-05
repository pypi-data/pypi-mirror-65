import aiohttp
import random
from .. import sr, sr_im

class Client:
    
    def __init__(self, proxies=None):
        if isinstance(proxies, type(None)):
            self.proxies = None
        elif isinstance(proxies, str):
            self.proxies = [proxies]
        elif isinstance(proxies, list):
            self.proxies = proxies

    async def search(self, q, **kwargs):
        if self.proxies:
            proxy = random.choice(self.proxies) if self.proxies else None
        async with aiohttp.ClientSession() as session:
            r = await session.get('https://www.bing.com/search', params=dict(q=q, **kwargs))
            data = await r.read()
        return sr(data)
    
    async def image(self, q, **kwargs):
        if self.proxies:
            proxy = random.choice(self.proxies) if self.proxies else None
        async with aiohttp.ClientSession() as session:
            r = await session.get('https://www.bing.com/images/search', params=dict(q=q, **kwargs))
            data = await r.read()
        return sr_im(data)