# 为什么需要 try？

先看一个例子。

```
print("开始")
num = int(input("请输入数字："))
print(100 / num)
print("结束")
```

如果输入: 10

输出: 开始 10 10.0 结束

没有问题。

但是输入: 0

程序会报错 `ZeroDivisionError: division by zero` 程序立即停止。

后面的 `print("结束")` 根本不会执行。这就是没有异常处理的问题。

# 最基本的 try

语法

```
try:
    可能出错的代码
except:
    出错以后执行这里
```

例如

```
try:
    num = int(input("请输入数字："))
    print(100 / num)
except:
    print("发生错误")
```

如果输入: 0

输出 `发生错误` 程序不会崩溃。

# try 的执行流程

假设

```
try:
    print("A")
    print(10 / 0)
    print("B")
except:
    print("C")

print("D")
```

执行顺序：

A ➡ 10/0 出错 ➡ 跳到 `except` ➡ C ➡ 继续执行 ➡ D ➡   ➡  ➡  ➡

所以输出: `A C D`

注意：

B 永远不会执行 因为异常发生以后，Python 会立即离开 try。

# except Exception as e

企业开发几乎都是这样写。

```
try:
    ...
except Exception as e:
    print(e)
```

例如

```
try:
    print(10 / 0)
except Exception as e:
    print(e)
```

输出 `division by zero`

这里 `e` 就是异常对象。

可以打印 `division by zero` 也可以写日志。

例如

`print(type(e))`

输出

`<class 'ZeroDivisionError'>`

# 多个 except

例如

```
try:
    num = int(input())
    print(100 / num)

except ValueError:
    print("输入不是数字")

except ZeroDivisionError:
    print("不能除0")
```

输入 `abc` 

输出 `输入不是数字`

输入 `0`

输出 `不能除0`

这就是针对不同异常分别处理。

# else

很多人不知道。

语法

```
try:
    ...
except:
    ...
else:
    ...
```

意思：只有没有发生异常才执行 else。

例如

```
try:
    print(10 / 2)
except:
    print("错误")
else:
    print("成功")
```

输出

```
5.0
成功
```

如果 `10 / 0`

输出

```
错误
```

不会进入 else。

# finally

这是网络自动化最常用的。

语法

```
try:
    ...
except:
    ...
finally:
    ...
```

意思：无论是否发生异常，finally 都一定执行。

例如

```
try:
    print(10 / 0)
except:
    print("发生错误")
finally:
    print("程序结束")
```

输出

```
发生错误
程序结束
```

即使没有异常

```
try:
    print(10 / 2)
except:
    print("错误")
finally:
    print("结束")
```

输出

```
5.0
结束
```

finally 永远执行。

# 为什么 Netmiko 一定要 finally？

例如 `connection = ConnectHandler(...)` 如果 `send_config_set()` 报错，如果没有 `connection.disconnect()` SSH 会话可能一直保持连接。所以企业代码一般写成 `connection = None`

```
try:
    connection = ConnectHandler(**device)

    ...

except Exception as e:
    print(e)

finally:
    if connection:
        connection.disconnect()
```

这就是企业代码标准。

# 完整执行流程

```
try:
    print("A")

except:
    print("B")

else:
    print("C")

finally:
    print("D")

print("E")
```

没有异常 ACED

有异常 ABDE 

注意：

else 不执行

# CCIE Enterprise Automation 中的实际应用

在网络自动化中，try 常用于处理各种可能失败的操作，例如：

| 操作              | 可能发生的异常         |
| --------------- | --------------- |
| SSH 登录设备        | 认证失败、超时、连接拒绝    |
| 下发配置            | 配置命令错误、权限不足     |
| 执行 `show` 命令    | 命令不存在、设备返回异常    |
| 读取 YAML/JSON 文件 | 文件不存在、格式错误      |
| 调用 REST API     | HTTP 错误、超时、连接失败 |


因此，一个典型的 Netmiko 脚本通常采用如下结构：

```
connection = None

try:
    connection = ConnectHandler(**device)
    connection.enable()

    output = connection.send_config_set(commands)
    print(output)

except Exception as e:
    print(f"Error: {e}")

finally:
    if connection:
        connection.disconnect()
```

这也是企业项目中最常见、最推荐的异常处理模式。