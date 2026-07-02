
# Learning Objectives

完成本节后，你应该能够：

- 理解什么是字符串（String）

- 创建字符串

- 使用字符串常用方法（Methods）

- 使用字符串拼接

- 使用 f-string（推荐）

- 理解字符串不可变（Immutable）

- 在网络自动化中处理字符串

## 创建字符串

```
hostname = "R1"
hostname = 'R1'
```

都可以创建字符串, 为了统一规范都使用 `"`

## String Methods (字符串方法)

```
hostname = "router1"
print(hostname.upper())
```

`.upper()` 是一种 Method 

`conn.send_command()` 也是字符串方法, 对象.方法()

`.upper()` 全大写

`.lower()` 全小写

`.replace()` 替换

`hostname.replace("R", "Router")` 将 R 替换为 Router

`.strip()` 去掉前后空格

## String Concatenation（字符串拼接）

```
hostname = "R1"
print("Device: " + hostname)
```

输出：

`Device: R1`

## f-string（推荐）

Python 3 推荐：

```
hostname = "R1"
print(f"Device: {hostname}")
```

输出：

`Device: R1`

为什么推荐？

因为以后：

```
ip = "10.1.1.1"
print(f"{hostname} -> {ip}")
```

非常直观。

Cisco 官方示例大量使用这种写法。

## String 是 Immutable（不可变）

这是一个非常重要的概念。

来看：

```
hostname = "R1"
hostname.upper()
print(hostname)
```

这属于一种错误写法, 这是创建了一个新的字符串。

正确写法：

```
hostname = hostname.upper()
print(hostname)
```

（如果原字符串是 "router1"，这里会输出 "ROUTER1"。）

这就是 Immutable。

## Cisco Automation Example

以后我们经常会收到 CLI 输出：

`GigabitEthernet0/0 is up`

如果想判断：

是不是：

UP

可以：

```
status = "GigabitEthernet0/0 is up"
print(status.upper())
```

输出：

`GIGABITETHERNET0/0 IS UP`

统一大小写以后，后续进行字符串比较时更方便。