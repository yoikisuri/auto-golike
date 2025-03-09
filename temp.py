import os
import random
import sys
import time

import requests


def main():
    while True:
        os.system("clear")

        # print("Nhập authorization golike của bạn vào để đăng nhập!")
        # auth = input("> ")

        headers = {
            "accept-language": "vi-VN,vi;q=0.9,en-US;q=0.8,en;q=0.7",
            "authorization": "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJodHRwOlwvXC9nYXRld2F5LmdvbGlrZS5uZXRcL2FwaVwvbG9naW4iLCJpYXQiOjE3NDEzNTA4NDUsImV4cCI6MTc3Mjg4Njg0NSwibmJmIjoxNzQxMzUwODQ1LCJqdGkiOiJsZTROS1htdE53RjA3MTFLIiwic3ViIjoyOTYxMzI1LCJwcnYiOiJiOTEyNzk5NzhmMTFhYTdiYzU2NzA0ODdmZmYwMWUyMjgyNTNmZTQ4In0.Nrxg7qur9HOk2Fw1Zx60P5x1emR4ABH9lONxIEL24UA",
            "content-type": "application/json;charset=utf-8",
            "t": "VFZSak1FMVVUVEZOUkd0NFRrRTlQUT09",
            "user-agent": random.choice(open("useragent.txt", "r").readlines()).strip()
        }

        user_data = requests.get(
            "https://gateway.golike.net/api/users/me", headers=headers, timeout=5
        ).json()
        if user_data.get("data", []):
            print(f"Đăng nhập thành công, Tài khoản: {user_data['data']['name']}")
            time.sleep(2)
            break
        print("Đăng nhập thất bại, kiểm tra lại authorization!")
        time.sleep(2)
    
    list_username = []
    list_id = []
    while True:
        os.system("clear")
        tiktok_account = requests.get("https://gateway.golike.net/api/tiktok-account", headers=headers, timeout=5).json()
        # print(tiktok_account)
        for idx, account in enumerate(tiktok_account["data"], start=1):
            list_username.append(account["nickname"])
            list_id.append(account["id"])
            print(f"{idx} - Tên: {account['nickname']}")
        print(f"Lựa chọn tài khoản chạy tool\nVí dụ: Nhập 1 để chọn tài khoản {list_username[0]} !")
        choose_account = int(input("> "))
        if 1 <= choose_account <= len(tiktok_account["data"]):
            print(f"Bạn đã chọn tài '{list_username[choose_account - 1]}' để chạy tool")
            break
        print("Sai! chọn lại tài khoản")
        time.sleep(2)

    while True:
        print("Nhập số lượng job bạn muốn chạy\nNếu bạn nhập 100 thì khi đến 100 job tool sẽ dừng")
        count_task = int(input("> "))
        for i in range(count_task):
            list_job = requests.get(f"https://gateway.golike.net/api/advertising/publishers/tiktok/jobs?account_id={list_id[choose_account - 1]}&data=null", headers=headers, timeout=5).json()
            # print(list_job)
            if "data" in list_job:
                url = list_job["data"]["link"]
                ads_id = list_job["data"]["id"]
                object_id = list_job["data"]["object_id"]
                type_job = list_job["data"]["type"]

                print(url, type_job)

                # chuyen sang tiktok
                os.system(f"termux-open {url}")

                for i in range(10, -1, -1):
                    print(f"Vui lòng chờ {i} giây để tiếp tục!", end=" \r")

                    time.sleep(1)

                print("Đang hoàn thành nhiệm vụ!")

                payloads = {
                    'ads_id' : ads_id,
                    'account_id' : list_id[choose_account - 1],
                    'object_id' : object_id ,
                    'async': 'true',
                    'data': 'null',
                    'type': type_job,
                }
                
                # vong lap nhan tien neu nhan that bai
                for i in range(5): # 5 lan neu that bai thi bo qua
                    complete_job = requests.post("https://gateway.golike.net/api/advertising/publishers/tiktok/complete-jobs", params=payloads, headers=headers, timeout=5).json()
                    #print(complete_job)
                    if complete_job["status"] == 200:
                        time.sleep(1)
                        print(f"Nhận tiền thành công! +{complete_job['data']['prices']}")
                        break
                    print(f"Nhận tiền thất bại lần {i}, đang thử lại!", end=" \r")
                    time.sleep(1)
                else:
                    print(f"Thất bại quá 5 lần, bỏ qua nhiệm vụ này!")
                    time.sleep(1)

                    skip_job = requests.post("https://gateway.golike.net/api/advertising/publishers/tiktok/skip-jobs", params=payloads, headers=headers, timeout=5).json()
                    print(skip_job)

                    time.sleep(1)


if __name__ == "__main__":
    main()
