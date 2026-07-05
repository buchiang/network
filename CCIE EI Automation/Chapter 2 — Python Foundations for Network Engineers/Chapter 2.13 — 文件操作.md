
这一节的重要程度 ⭐⭐⭐⭐⭐

为什么？因为企业自动化每天都在读文件, 写文件。

例如：

```
backup/
├──R1.cfg
├──R2.cfg
├──R3.cfg
```

是不是全部都是File。

# Learning Objectives

完成这一节以后你应该能够：

- 打开文件

- 写文件

- 读取文件

- 自动生成配置备份

- 为 Netmiko Backup 做准备

Python 最经典一句 `with open(...)` 很多人第一次看见觉得特别难。其实一点都不难。

## 第一步

创建：

```
file = open(
    "test.txt",
    "w"
)
```

这里 `open()` 返回什么? 很多教程不会讲。其实返回一个 `File Object`

这里 "w" 是文件开打模式 File Mode 决定 Python 以什么方式操作这个文件

1. "r" —— Read（读取）

2. "w" —— Write（写入）

3. "a" —— Append（追加）

4. "x" —— Exclusive Create（独占创建）

所以：

file ➡ File Object

是不是很熟悉？前面我们已经见过 String Object, Dictionary Object, ConnectHandler Object

现在只是又来了一个 File Object

## File Object

它有哪些 Method？

例如：

```
file.write()
file.read()
file.close()
```

是不是又是对象 ➡ 方法所以 Python 真的只有一种思想 Everything is an Object

## 为什么：

不用 `close()` 而写 `file.close()` 因为 `close()` 属于File Object 不是 Python。

## 写文件

例如：

```
file = open(
    "backup.txt",
    "w"
)

file.write(
    "hostname R1"
)
```

`file.close()`

结果生成 backup.txt 内容 hostname R1

## 但是：

企业里面基本不会这样写。因为如果程序中途 Crash。`close()` 没有执行。文件一直打开。这叫 Resource Leak 资源泄漏。

## 企业真正写法

Python：

推荐：

```
with open(
    "backup.txt",
    "w"
) as file:

    file.write(
        "hostname R1"
    )
```

没有 `close()` 为什么？因为 with 结束。Python 自动 close。

这是 Chapter 2 目前最重要的新知识。以后你会看到 `with ConnectHandler(...)` 是不是很像？其实原理一样。

## Cisco Automation Example

以后真正 Backup

就是：

```
output = conn.send_command(
    "show running-config"
)
```

然后：

```
with open(
    "R1.cfg",
    "w"
) as file:

    file.write(output)
```

结束。

是不是 Backup 已经完成？


## Lab 2.13

在 Linux 中运行 [lab2.13.py](python/lab2.13.py)


然后 Linux `cat R1.cfg`

你会看到：

```
hostname R1

interface Loopback0
 ip address 1.1.1.1 255.255.255.255
```

## Observe → Verify → Analyze

请注意我们不是打印配置。而是真正生成 R1.cfg 这就是企业真正做 Backup。

## CCIE Engineer Insight

这里我要提前告诉你一个工程实践。

很多网络工程师会写 `with open("backup.txt", "w")` 以后100 台设备. 全部写 backup.txt 最后只剩最后一台设备。

正确应该：

```
filename = (
    f"{device['hostname']}.cfg"
)

然后：

with open(
    filename,
    "w"
) as file:

    file.write(output)
```

最后得到：

```
backup/
├──R1.cfg
├──R2.cfg
├──R3.cfg
```

这就是企业每天都在做的配置备份。