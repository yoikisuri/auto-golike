import asyncio
import os
import random
import time

import aiohttp

from utils import countdown


class SnapChat:
    def __init__(self, auth) -> None:
        self.auth = auth
        self.headers = {
            "accept-language": "vi-VN,vi;q=0.9,en-US;q=0.8,en;q=0.7",
            "authorization": "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJodHRwOlwvXC9nYXRld2F5LmdvbGlrZS5uZXRcL2FwaVwvbG9naW4iLCJpYXQiOjE3NDEzNTA4NDUsImV4cCI6MTc3Mjg4Njg0NSwibmJmIjoxNzQxMzUwODQ1LCJqdGkiOiJsZTROS1htdE53RjA3MTFLIiwic3ViIjoyOTYxMzI1LCJwcnYiOiJiOTEyNzk5NzhmMTFhYTdiYzU2NzA0ODdmZmYwMWUyMjgyNTNmZTQ4In0.Nrxg7qur9HOk2Fw1Zx60P5x1emR4ABH9lONxIEL24UA",
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

    async def job(self):
        async with aiohttp.ClientSession() as session:
            url = "https://gateway.golike.net/api/advertising/publishers/snapchat/jobs"
            params = {
                "account_id": "2543",
            }
            async with session.request(
                "GET", url, params=params, headers=self.headers
            ) as response:
                return await response.json()

    async def complete(self, ads_id):
        async with aiohttp.ClientSession() as session:
            url = "https://gateway.golike.net/api/advertising/publishers/snapchat/complete-jobs"
            data = {
                "account_id": 2543,
                "ads_id": ads_id,
            }
            async with session.request(
                "POST", url, headers=self.headers, json=data
            ) as response:
                return await response.json()

    async def skip_job(self, ads_id, object_id):
        async with aiohttp.ClientSession() as session:
            url = "https://gateway.golike.net/api/advertising/publishers/snapchat/skip-jobs"
            data = {
                "account_id": 2543,
                "ads_id": ads_id,
                "object_id": f"{object_id}",
            }
            async with session.request(
                "POST", url, headers=self.headers, json=data
            ) as response:
                return await response.json()


class Client:
    def __init__(self) -> None:
        self.client = None
        self.auth = None

    async def run(self):
        users = await SnapChat(self.auth).users()
        snapchat = await SnapChat(self.auth).snapchat()
        print(users)
        print(snapchat)

        count = 5
        for index in range(5):
            job = await SnapChat(self.auth).job()
            if job["status"] == 200:
                url = job["data"]["link"]
                ads_id = job["data"]["id"]
                object_id = job["data"]["object_id"]
                type_ = job["data"]["type"]

                print(f"{type_.upper()} - {object_id} - {url}")

                os.system(f"termux-open {url}")

                countdown(10)

                complete = await SnapChat(self.auth).complete(ads_id)
                print(
                    f"[{index}/{count}][{time.time()}][THÀNH CÔNG][+{complete['data']['prices']}]"
                )


if __name__ == "__main__":
    asyncio.run(Client().run())
