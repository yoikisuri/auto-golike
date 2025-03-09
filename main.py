import asyncio
import os
import random

import aiohttp

from utils import fetch


class GolikeApi:
    def __init__(self,auth) -> None:
        self.auth = auth
        self.headers = {
            "accept-language": "vi-VN,vi;q=0.9,en-US;q=0.8,en;q=0.7",
            "authorization": "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJodHRwOlwvXC9nYXRld2F5LmdvbGlrZS5uZXRcL2FwaVwvbG9naW4iLCJpYXQiOjE3NDEzNTA4NDUsImV4cCI6MTc3Mjg4Njg0NSwibmJmIjoxNzQxMzUwODQ1LCJqdGkiOiJsZTROS1htdE53RjA3MTFLIiwic3ViIjoyOTYxMzI1LCJwcnYiOiJiOTEyNzk5NzhmMTFhYTdiYzU2NzA0ODdmZmYwMWUyMjgyNTNmZTQ4In0.Nrxg7qur9HOk2Fw1Zx60P5x1emR4ABH9lONxIEL24UA",
            "content-type": "application/json;charset=utf-8",
            "t": "VFZSak1FMVVUVEZOUkd0NFRrRTlQUT09",
            "user-agent": random.choice(
                open("useragent.txt", "r").readlines()
            ).strip(),
        }

    async def get_user(self):
        url = "users/me"
        async with aiohttp.ClientSession() as session:
            return await fetch(session, url, headers=self.headers)
    async def get_tiktok_account(self):
        url = "tiktok-account"
        async with aiohttp.ClientSession() as session:
            return await fetch(session, url, headers=self.headers)
    
    async def get_list_task(self, account_id):
        url = f"advertising/publishers/tiktok/jobs?account_id={account_id}&data=null"
        async with aiohttp.ClientSession() as session:
            return await fetch(session, url, headers=self.headers)

    async def receive_money(self, ads_id, account_id, object_id, type):
        url = f"advertising/publishers/tiktok/complete-jobs"
        json_data = {
            'ads_id' : ads_id,
            'account_id' : account_id,
            'object_id' : f"{object_id}",
            'type': type,
        }
        async with aiohttp.ClientSession() as session:
            return await fetch(session, url, method="POST", data=json_data, headers=self.headers)

    async def skip_task(self, ads_id, account_id, object_id, type):
        url = f"advertising/publishers/tiktok/skip-jobs"
        json_data = {
            'ads_id' : ads_id,
            'account_id' : account_id,
            'object_id' : f"{object_id}",
            'type': type,
        }
        async with aiohttp.ClientSession() as session:
            return await fetch(session, url, method="POST", data=json_data, headers=self.headers)
        
class GolikeClient:
    def __init__(self) -> None:
        self.auth = None
        self.client = None
        self.account_id = []

    async def login(self):
        while True:
            os.system("clear")
            if os.path.exists("user.txt"):
                auth = open("user.txt","r").read()
                result = (await GolikeApi(auth).get_user())
                print(result)
                if result["status"] == 200 and result["data"] != []:
                    print(f"Đăng nhập thành công, Tài khoản: {result['data']['name']}")
                    await asyncio.sleep(2)
                    choose = input("Bạn có muốn thay đổi tài khoản không? (y/N): ")
                    if choose.upper() == "N" or not choose:
                        self.auth = auth
                        break
                    os.remove("user.txt")
                print("Đăng nhập thất bại, đang xóa thông tin cũ!")
                os.remove("user.txt")
                await asyncio.sleep(2)

            else:
                auth = input("Nhập Authorization: ")
                result = (await GolikeApi(auth).get_user())
                print(result)
                if result["status"] == 200 and result["data"] != []:
                    print(f"Đăng nhập thành công, Tài khoản: {result['data']['name']}")
                    with open("user.txt","w+") as fauth:
                        fauth.write(auth)
                    await asyncio.sleep(2)
                    self.auth = auth
                    break
                print("Đăng nhập thất bại, nhập lại authorization!")
                await asyncio.sleep(2)

    async def account(self):
        while True:
            os.system("clear")

            result = (await GolikeApi(self.auth).get_tiktok_account())
            print(result)
            for index, account in enumerate(result["data"], 1):
                self.account_id.append(account['id'])
                print(f"{index}, {account['nickname']}")
            choose = int(input("Chọn tài khoản chạy tool: "))
            if 1 <= choose <= len(result["data"]):
                print(f"Bạn đã chọn tài khoản tiktok: {self.account_id[choose - 1]}")
                await asyncio.sleep(2)
                self.choose = choose
                break
            else:
                print("Lựa chọn không hợp lệ, Hãy chọn lại!")
                await asyncio.sleep(2)
    async def complete_task(self):
        while True:
            os.system("clear")
            
            account_id = self.account_id[self.choose - 1]
            result = (await GolikeApi(self.auth).get_list_task(account_id))
            print(result)
            
            if result["status"] == 200:
                url = result["data"]["link"]
                ads_id = result["data"]["id"]
                object_id = result["data"]["object_id"]
                type = result["data"]["type"]

                print(ads_id, object_id, type)
                os.system(f"termux-open {url}")

                for countdown in range(10, -1, -1):
                    print(f"Vui lòng chờ {countdown} giây nữa để tiếp tục!", end=" \r")
                    await asyncio.sleep(1)

                result = (await GolikeApi(self.auth).receive_money(ads_id, object_id, type, account_id))
                print(result)

                # 
                if result["status"] == 200:
                    print(f"Nhận tiền thành công +{result['data']['prices']}đ")
                    await asyncio.sleep(2)
                else:
                    print("Nhận tiền thất bại, đang thử lại...", end="\r")

                    await asyncio.sleep(2)
                    result = (await GolikeApi(self.auth).receive_money(ads_id, object_id, type, account_id))
                    print(result)

                    if result["status"] == 200:
                        print(f"Nhận tiền thành công +{result['data']['prices']}đ")
                        await asyncio.sleep(2)
                    else:
                        print("Thất bại, đang skip nhiệm vụ!")
                        result = (await GolikeApi(self.auth).skip_task(ads_id, object_id, account_id, type))
                        print(result)

                        await asyncio.sleep(2)



    async def run(self):
        await self.login()
        await self.account()
        await self.complete_task()


if __name__ == "__main__":
    asyncio.run(GolikeClient().run())
