from time import sleep
import aiohttp, asyncio, random, os
from utils import fetch


class GOLIKE:
    def __init__(self) -> None:
        self.headers = {
            "accept-language": "vi",
            "authorization": "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJodHRwOlwvXC9nYXRld2F5LmdvbGlrZS5uZXRcL2FwaVwvbG9naW4iLCJpYXQiOjE3NDEzNTA4NDUsImV4cCI6MTc3Mjg4Njg0NSwibmJmIjoxNzQxMzUwODQ1LCJqdGkiOiJsZTROS1htdE53RjA3MTFLIiwic3ViIjoyOTYxMzI1LCJwcnYiOiJiOTEyNzk5NzhmMTFhYTdiYzU2NzA0ODdmZmYwMWUyMjgyNTNmZTQ4In0.Nrxg7qur9HOk2Fw1Zx60P5x1emR4ABH9lONxIEL24UA",
            "content-type": "application/json;charset=utf-8",
            "t": "VFZSak1FMVVUVEZOUkd0NFRrRTlQUT09",
            "user-agent": random.choice(open("useragent.txt", "r").readlines()).strip(),
        }

    async def run(self):
        url = "https://gateway.golike.net/api/users/me"
        user_me = await fetch(url=url, headers=self.headers, method="GET")

        print(user_me)

        url = "https://gateway.golike.net/api/tiktok-account"
        tktt = await fetch(url, self.headers, "GET")

        print(tktt)
        account_id = tktt["data"][0]["id"]

        while True:
            url = "https://gateway.golike.net/api/advertising/publishers/tiktok/jobs"
            params = {"account_id": account_id, "data": "null"}

            listjob = await fetch(url, self.headers, "GET", params)

            ads_id = listjob["data"]["id"]
            object_id = listjob["data"]["object_id"]
            type_ = listjob["data"]["type"]
            url = listjob["data"]["link"]
            
            print(account_id, ads_id, object_id, type_)

            os.system(f"termux-open {url}")

            await asyncio.sleep(10)

            url = "https://gateway.golike.net/api/advertising/publishers/tiktok/complete-jobs"
            data = {
                "ads_id": ads_id,
                "account_id": account_id,
                "object_id": f"{object_id}",
                "async": "true",
                "data": "null",
                "type": type_,
            }
            nhan_tien = await fetch(url, self.headers, "POST", data)
            print(nhan_tien)
            nhan_tien = await fetch(url, self.headers, "POST", data)
            print(nhan_tien)
            nhan_tien = await fetch(url, self.headers, "POST", data)
            print(nhan_tien)
            if nhan_tien["status"] == 200:
                print(nhan_tien["data"]["prices"])
            else:
                url = "https://gateway.golike.net/api/advertising/publishers/tiktok/skip-jobs"
                skip = await fetch(url, self.headers, "POST", data)
                print(skip)


if __name__ == "__main__":
    asyncio.run(GOLIKE().run())
