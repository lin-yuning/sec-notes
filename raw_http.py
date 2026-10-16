import socket

# 1. 建立 TCP 连接（这一步背后就是"三次握手"，后面再细讲）
s = socket.create_connection(("www.baidu.com", 80), timeout=10)

# 2. 手写一个原始 HTTP 请求 —— 注意，它就是一段纯文本
request = b"GET / HTTP/1.0\r\nHost: www.baidu.com\r\n\r\n"
s.sendall(request)

# 3. 循环收数据，直到对方关闭连接
data = b""
while True:
    chunk = s.recv(4096)
    if not chunk:
        break
    data += chunk
s.close()

# 4. HTTP 用"空行"把响应头和响应体分开
head, _, body = data.partition(b"\r\n\r\n")

print("=== RESPONSE HEADERS ===")
print(head.decode("ascii", "replace"))
print()
print("=== BODY SIZE: %d bytes ===" % len(body))
print("=== FIRST 150 BYTES OF BODY ===")
print(body[:150])
