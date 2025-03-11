import asyncio
import os
import sys
import time

from utils import *


class GolikeClient:
    def __init__(self) -> None:
        self.total = 0
        self.account_ids = []

    async def main(self):
        while True:
            os.system("clear")

            if os.path.exists("user.txt"):
                with open("user.txt", "r") as f:
                    self.auth = f.read()

                self.client = SnapChat(self.auth)
                user_data = await self.client.users()

                if user_data["status"] == 200:
                    print(
                        f"Đăng nhập thành công! Tài Khoản: {user_data['data']['name']}"
                    )
                    with open("user.txt", "w") as f:
                        f.write(self.auth)
                        await asyncio.sleep(2)
                        break

                print(f"Đăng nhập thất bại! Kiểm tra lại authorization")
                await asyncio.sleep(2)
                os.remove("user.txt")

            else:
                self.auth = input("Nhập Authorization: ")
                self.client = SnapChat(self.auth)
                user_data = await self.client.users()

                if user_data["status"] == 200:
                    print(
                        f"Đăng nhập thành công! Tài Khoản: {user_data['data']['name']}"
                    )
                    with open("user.txt", "w") as f:
                        f.write(self.auth)
                        await asyncio.sleep(2)
                        break

                print(f"Đăng nhập thất bại! Kiểm tra lại authorization")
                await asyncio.sleep(2)
        while True:
            os.system("clear")

            snapchat = await self.client.snapchat()
            for i, snapchat in enumerate(snapchat["data"], 1):
                # print(snapchat)
                self.account_ids.append(snapchat["id"])
                print(f"Tài khoản: {i} / Tên: {snapchat['name']}")
            choose = input(f"Chọn tài khoản snapchat: ")
            if 1 <= int(choose) <= len(self.account_ids):
                self.account_id = self.account_ids[int(choose) - 1]
                break
            print("Không hợp lệ! Hãy nhập lại lựa chọn")
            await asyncio.sleep(2)
        while True:
            count = input(
                "Nhập số job bạn muốn làm ( nhập 100 thì tới job 100 sẽ dừng tool ): "
            )
            for i in range(int(count)):
                jobs = await self.client.job()

                if jobs["status"] == 200:
                    url = jobs["data"]["link"]
                    ads_id = jobs["data"]["id"]
                    object_id = jobs["data"]["object_id"]
                    type_ = jobs["data"]["type"]

                    print(f"Nhiệm vụ: {type_.upper()} / url job: {url}")

                    os.system(f"termux-open {url}")

                    countdown(10)

                    receive = await self.client.complete(self.account_id, ads_id)

                    if receive["status"] == 200:
                        self.total += int(receive["data"]["prices"])
                        print(
                            f"{i} / Thành công! +{receive['data']['prices']}Đ / Tổng: {self.total}"
                        )
                    else:
                        for i in range(5):
                            print(f"Nhận thất bại! Đang thử lại lần {i}", end="\r")
                            receive = await self.client.complete(
                                self.account_id, ads_id
                            )
                            if receive["status"] == 200:
                                self.total += receive["data"]["prices"]
                                print(
                                    f"{i} / Thành công! +{receive['data']['prices']}Đ / Tổng: {self.total}"
                                )
                                break
                        else:
                            skip = await self.client.skip_job(self.account_id, ads_id, object_id)
                            print(skip)


if __name__ == "__main__":
    asyncio.run(GolikeClient().main())
