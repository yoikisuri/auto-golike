import aiohttp


async def fetch(session, url, headers, method="GET", params=None, data=None):
    """
    Hàm gửi request với phương thức GET hoặc POST.

    - session: Đối tượng aiohttp.ClientSession.
    - url: Đường dẫn API.
    - headers: Headers của request.
    - method: GET hoặc POST (bắt buộc).
    - params: Query parameters (tùy chọn).
    - data: Dữ liệu gửi lên nếu là POST (tùy chọn).
    """

    base_url = "https://gateway.golike.net/api/" + url
    method = method.upper()
    if method not in ["GET", "POST"]:
        raise ValueError("Method phải là 'GET' hoặc 'POST'")

    async with session.request(
        method, base_url, headers=headers, params=params, json=data
    ) as response:
        return await response.json()
