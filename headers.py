"""Day 5 练习：用 requests 发一次 HTTP 请求，看状态码和安全相关的响应头。"""

import requests

url = input("网址: ").strip()
r = requests.get(url, timeout=10)

print("状态码:", r.status_code)
print("正文长度:", len(r.text))

# 和安全最相关的几个响应头
for name, value in r.headers.items():
    print(f"{name}: {value}")
print("跳转次数:", len(r.history))
print("Cookie:", r.cookies.get_dict())