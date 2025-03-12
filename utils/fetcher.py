import random

import aiohttp


class SnapChat:
    def __init__(self, auth) -> None:
        self.auth = auth
        self.headers = {
            "accept-language": "vi-VN,vi;q=0.9,en-US;q=0.8,en;q=0.7",
            "authorization": self.auth,
            "content-type": "application/json;charset=utf-8",
            "t": "VFZSak1FMVVXWGxOVkZFeFRYYzlQUT09",
            "user-agent": random.choice(open("useragent.txt", "r").readlines()).strip(),
        }

    async def users(self):
        async with aiohttp.ClientSession() as session:
            url = "https://gateway.golike.net/api/users/me"
            async with session.request("GET", url, headers=self.headers) as response:
                return await response.json()

    async def snapchat(self):
        async with aiohttp.ClientSession() as session:
            url = "https://gateway.golike.net/api/snapchat-account"
            async with session.request("GET", url, headers=self.headers) as response:
                return await response.json()

    async def job(self, account_id):
        async with aiohttp.ClientSession() as session:
            url = "https://gateway.golike.net/api/advertising/publishers/snapchat/jobs"
            params = {
                "account_id": account_id,
            }
            async with session.request(
                "GET", url, params=params, headers=self.headers
            ) as response:
                return await response.json()

    async def complete(self, account_id, ads_id):
        async with aiohttp.ClientSession() as session:
            url = "https://gateway.golike.net/api/advertising/publishers/snapchat/complete-jobs"
            data = {
                "account_id": account_id,
                "ads_id": ads_id,
            }
            async with session.request(
                "POST", url, headers=self.headers, json=data
            ) as response:
                return await response.json()

    async def skip_job(self, account_id, ads_id, object_id):
        async with aiohttp.ClientSession() as session:
            url = "https://gateway.golike.net/api/advertising/publishers/snapchat/skip-jobs"
            data = {
                "account_id": account_id,
                "ads_id": ads_id,
                "object_id": f"{object_id}",
            }
            async with session.request(
                "POST", url, headers=self.headers, json=data
            ) as response:
                return await response.json()
