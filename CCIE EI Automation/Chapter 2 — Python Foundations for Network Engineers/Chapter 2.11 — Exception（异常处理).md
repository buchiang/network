
Exception 的重要程度高于 Tuple、Set、while。企业自动化最怕的不是配置失败，而是程序崩溃。

## 什么是 Exception？

很多教程说 Exception = 异常, 没有错。但是工程师理解应该是程序运行过程中发生的错误。

例如：`print(10 / 0)`

运行得到：`ZeroDivisionError`

程序：停止。

再例如：`print(hostname)`

如果：`hostname` 没有定义。

得到：`NameError`

程序：停止。

再例如以后：`ConnectHandler(...)`

设备：密码错误。

得到：`NetmikoAuthenticationException`

程序：停止。

## try / except

Python 提供 try 意思**我准备执行一些可能失败的代码**。

例如：

```
try:
    print(10 / 0)
```

如果失败。Python 立即跳到 `except`

例如：

```
try:
    print(10 / 0)

except:
    print("Something went wrong")
```

输出：`Something went wrong`

程序：继续。

## 为什么不能一直用 except？

很多初学者喜欢：

```
try:
    ...

except:
    print("Error")
```

这是企业里面非常不推荐的写法。因为你不知道到底发生了什么。

例如可能是：

- 密码错误

- IP 写错

- SSH 超时

- DNS 失败

- 程序 Bug

全部变成 `Error`没有任何价值。

## 正确写法

例如：

```
try:
    print(10 / 0)

except ZeroDivisionError:
    print("Cannot divide by zero")
```

以后 Netmiko 也是一样。

例如：

```
try:
    conn = ConnectHandler(**device)

except NetmikoAuthenticationException:
    print("Authentication Failed")
```

以后 Chapter 3 就会写这个。

## Exception Object

更进一步 Python 允许 `except Exception as e`

例如：

```
try:
    print(10 / 0)

except Exception as e:
    print(e)
```

输出：

`division by zero`

注意 `e` 是什么？也是对象。里面保存错误信息。所以以后 `print(type(e))`

得到：

`Exception Object`

## Cisco Automation Example

以后真正企业代码长这样：

```
for device in devices:

    try:

        conn = ConnectHandler(**device)

        output = conn.send_command(
            "show version"
        )

        print(output)

        conn.disconnect()

    except Exception as e:

        print(
            f"{device['hostname']} failed"
        )

        print(e)
```

是不是即使 R37 失败。程序仍然继续 R38。

## 为什么 Exception 比 if 更重要？

很多初学者第一反应 `if login_failed` 问题是连接失败的时候，程序已经抛出了 Exception。根本不会返回 `login_failed` 所以网络自动化首先学 `Exception`。不是 `if`。

## Lab 2.11

运行 [lab11.py](python/lab11.py) 你会看到：

```
Connecting R1
Success
------------------------------

Connecting R2
Failed: SSH Authentication Failed
------------------------------

Connecting R3
Success
------------------------------
```

请注意 R2 失败。但是 R3 继续。这就是Exception 的意义。

## 企业里面真正的写法

以后不会 `print()` 而是 `logging.error(...)` 或者 `logger.exception(...)` 我们在 Chapter 4（工程化）再学习 Logging。

# CCIE Engineer Insight（本章最重要）

Review 自动化代码时，最关注的不是会不会写 `ConnectHandler()`。而是失败的时候怎么办？

一个成熟的自动化工程师，写代码时会先考虑：

- SSH 超时怎么办？

- 密码错误怎么办？

- 网络中断怎么办？

- 设备重启怎么办？

- 一台设备失败，是否影响其他设备？

真正稳定的自动化程序，不是永远成功，而是能够优雅地处理失败。