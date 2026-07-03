
# Learning Objectives

完成本节后，你应该能够：

- 理解为什么需要 Function

- 定义 Function

- 调用 Function

- 理解 Parameters（参数）

- 理解 Return Value（返回值）

- 在 Cisco Automation 中封装重复操作

def 不是简单的 definition 的缩写, 它的意思是 define a function 定义一个函数

## 调用（Call）

定义以后：

```
def hello():
    print("Hello CCIE")
```

函数不会自动执行。

必须：`hello()` 才会运行。

这是很多初学者第一次遇到的疑问： 为什么写了函数没有输出？

因为： 定义 ≠ 调用。

## Parameters（参数）

刚才的函数只能 `print("Hello")` 如果我要打印 `R1 R2 R3` 怎么办？

应该：

```
def connect(hostname):
    print(f"Connecting {hostname}")
```

调用：

```
connect("R1")
connect("R2")
connect("R3")
```

输出：

```
Connecting R1
Connecting R2
Connecting R3
```

注意这里 `hostname` 叫：**Parameter（形参）** 而 `connect("R1")` 这里 `R1` 叫 **Argument（实参）**很多教程把两者混着讲。以后我们严格区分。

## Return（返回值）

再看：

```
def get_hostname():
    return "R1"
```

这里 `return` 表示把结果返回。

例如：

```
hostname = get_hostname()
print(hostname)
```

输出：`R1` 所以 Function 不仅可以执行动作。还可以返回数据。

Cisco Automation Example 1

以后你可能写：

```
def backup(device):
    print(f"Backing up {device['hostname']}")
```

调用：

```
for device in devices:
    backup(device)
```

这里你会发现今天学的：

- List

- Dictionary

- for

- Function

全部串起来了。

## Lab 2.10

运行 [lab2.10.py](python/lab2.10.py) 你会发现：

和上一节输出完全一样。但是代码已经开始工程化。

## Analyze

请特别注意 `connect(device)` 这里传进去的是整个 `Dictionary`。不是 `device["hostname"]` 为什么？因为以后 `Function` 可能需要：

```
hostname
host
username
password
device_type
```

如果只传 `hostname`。以后还要不断增加参数：

```
connect(
    hostname,
    host,
    username,
    password,
    port,
    timeout,
    secret
)
```

越来越难维护, 而直接：

```
connect(device)
```

整个 Dictionary。以后增加新的字段。`Function` 几乎不用改。

# CCIE Engineer Insight（这一节最重要）

这是我过去十几年写网络自动化最大的经验之一, 传递对象，而不是传递一堆零散的数据。

例如不要这样：

```
backup(
    hostname,
    host,
    username,
    password
)
```

而是 `backup(device)` 因为 `device` 本身就代表一台设备。它是一个完整的业务对象。

这种设计有几个好处：

- 扩展性强：以后增加 port、secret、platform 等字段，不需要修改所有函数调用。

- 可读性好：看到 backup(device)，就知道这个函数处理的是一台设备。

- 符合主流自动化框架：Netmiko、NAPALM、Nornir 等框架都大量采用这种思路。