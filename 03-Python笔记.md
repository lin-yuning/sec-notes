# Python 起步：用 requests 发一次真实请求

> 状态行：`2026-10-22`　Day 5

---

## 今天做了什么

2026-10-22，Day 5。今天第一次用 Python 的 `requests` 库发真实 HTTP 请求，拿到了状态码、响应头、Cookie 三样东西。

前几天在 HTTP 笔记里抄的那些字段（`Server`、`Content-Type`、`Set-Cookie`），今天总算看到了真实报文——原来它们不是课本上的名词，是每打开一次网页，服务器真的会发过来的东西。

---

## 一段我亲手跑通的代码

```python
import requests                                  # 引入发请求的库

url = input("网址: ").strip()                    # 让用户输入地址，strip() 去掉首尾空格
r = requests.get(url, timeout=10)                # 发请求，最多等 10 秒

print("状态码:", r.status_code)                   # 200 表示成功
print("正文长度:", len(r.text))                   # 正文有多少个字符

for name, value in r.headers.items():            # 把响应头一条条打印出来
    print(f"{name}: {value}")

print("跳转次数:", len(r.history))                # 中间经过几次重定向
print("Cookie:", r.cookies.get_dict())           # 服务器塞给我的 Cookie
```

拿 `https://www.baidu.com` 跑，输出是：

```
状态码: 200
正文长度: 2443
Server: bfe
Content-Type: text/html
...（一共 8 个响应头）
跳转次数: 0
Cookie: {'BDORZ': '...'}
```

---

## 三个新概念

### 1. 缩进就是代码块

别的语言用 `{ }` 划分代码块，Python **用缩进**。同样的几行，往右移 4 格就变成另一个程序。

我今天真的踩到了：`print("跳转次数")` 多缩进了 4 格，结果它被算作 `for` 循环体的一部分，**每打印一个响应头就执行一次**——`api.github.com` 有 26 个响应头，这行就打印了 26 遍。

记住这条界线：

- 缩进 4 格 → 「我是上面那个 `for` 的身体」，每轮都执行
- 顶到最左边 → 「循环结束了」，往下继续走

### 2. `.items()` 与拆包

`r.headers` 不是普通字符串，而是一个「键→值」的容器。

- 直接 `for name in r.headers:` → 只能拿到**键**（`Server`、`Date` 这些名字）
- `for name, value in r.headers.items()` → 一次拿到**键和值**

`.items()` 的作用是把每一对「键、值」打包递出来；`name, value` 是 Python 的**拆包**写法，一次接住两个值。

### 3. 报错到底怎么读

**traceback 从下往上读，不是从上往下读。**

- 最后一行才是真正的错误：`TimeoutError: The read operation timed out`
- 中间那一堆 `File "..."` 是调用链，新手可以直接跳过
- 关键动作：**找第一行写着自己文件名的地方**（`File "headers.py", line N`）

如果通篇找不到自己的文件名，说明**代码没写错，是外部环境的问题**。今天那次超时就是这样——报错全在 `urllib3`、`ssl` 这些库里面，一行都没提到我的 `headers.py`。

---

## 我踩过的坑

### 坑 1：多缩进 4 格，打印了 26 遍

```
报错原文：（没有报错，只是输出重复了 26 次）
我以为：程序写错了
实际是：最后两条 print 缩进了 4 格，被算进了 for 循环体内
改法：把这两行顶到最左边，和 for 对齐
```

教学点：**Python 里错误不一定是红色的**。有时代码能跑，只是结果荒谬——这种叫「安静的错误」，比报错更难发现。

### 坑 2：连 github 超时

```
报错原文：TimeoutError: The read operation timed out
我以为：我的代码写坏了
实际是：www.github.com 从本机连不通（同机实测 api.github.com 1 秒通、github.com 超时）
改法：换一个能通的地址；并且学会区分 ConnectTimeout（连都没连上）和 ReadTimeout（连上了但对方不回话）
```

### 坑 3：403 不是被墙，是被限流

打开梯子后访问 `api.github.com` 返回 **403**：

```json
{"message":"API rate limit exceeded for 45.149.92.7. ..."}
```

响应头里写着 `X-RateLimit-Limit: 60`、`X-RateLimit-Remaining: 0`。

- `45.149.92.7` 是梯子的**出口 IP**，一个 IP 很多人共用
- GitHub 对未登录请求只给**每小时 60 次**
- 额度用完了，所以返回 403 而不是 429

安全含义：**频率限制是防密码爆破的第一道防线**。只按 IP 限的话，换个 IP 就绕过了；按「账号」或「IP+账号」限才有效。

---

## 今天最反直觉的一件事

我原以为写代码就是「把语法背对、敲进去、跑起来」。

今天发现真正花时间的不是写那 10 行，而是**读不懂的报错**和**看起来对但结果荒谬的输出**。写代码的功夫，一大半在读错误信息上。

---

## 命令速查

| 命令 / 写法 | 作用 | 什么时候用 |
| --- | --- | --- |
| `python 文件名.py` | 运行一个脚本 | 每次改完代码 |
| `pip install 库名` | 装第三方库（装进当前这个 python） | `import` 时报 ModuleNotFoundError |
| `pip install -i https://pypi.tuna.tsinghua.edu.cn/simple 库名` | 走清华镜像装 | 官方源太慢时 |
| `git add .` → `git commit -m "说明"` → `git push` | 存档并推到 GitHub | 每天收工 |

> VS Code 里 `Ctrl+Shift+V` 是 Markdown 预览，`Ctrl+S` 是保存——**不保存，程序读到的还是旧文件**。

---

## 下一步

明天 Day 6：WSL2 + Docker + DVWA 靶场。

开工前先确认一件事：**WSL 里有没有装发行版**。我这边只启用了 WSL 功能，没装 Ubuntu——直接上 Docker 会第一步就卡住。
