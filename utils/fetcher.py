import aiohttp

async def fetch(url, headers, method, params=None, data=None):
    async with aiohttp.ClientSession() as session:
        async with session.request(
            method, url, headers=headers, params=params, json=data
        ) as response:
            return await response.json()
