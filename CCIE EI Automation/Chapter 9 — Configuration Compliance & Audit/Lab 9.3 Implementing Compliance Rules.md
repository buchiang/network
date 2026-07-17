经过前两个实验, 我们已经拥有：

```
Inventory
      │
      ▼
Connection
      │
      ▼
Backup
      │
      ▼
Parser
      │
      ▼
Python Data
```

现在终于来到整个 Chapter 9 的核心利用 Parser 提供的数据, 实现 Enterprise Compliance Rules. 

## Lab Objective

本实验的目标新增：

```
modules/

    compliance.py
```

它负责 Python Data ➡ Evaluate ➡ PASS / FAIL

整个模块不解析配置, 不建立 SSH, 不保存文件, 只负责 Business Logic. 

## Compliance Module 的职责

再次强调整个 Framework 的职责划分：

| Module          | Responsibility    |
| --------------- | ----------------- |
| connection.py   | 建立 SSH            |
| backup.py       | 获取 Running Config |
| parser.py       | 提取配置数据            |
| compliance.py   | 判断是否符合 Baseline   |
| report.py（稍后实现） | 输出检查结果            |


整个 Workbook 一直坚持：

>每个模块只有一个职责. 

## Step 1 — 创建 compliance.py

新增：

```
modules/

    compliance.py
```

里面暂时只有几个检查函数. 

例如：

```python
check_hostname()

check_ntp()

check_logging()

check_banner()

check_ssh()

check_password_encryption()
```

## Step 2 — check_hostname()

企业 Baseline, Hostname 必须存在. Parser 返回 hostname = "R1" 或者 hostname = None

Compliance 判断：

```python
def check_hostname(hostname):
    return hostname is not None
```

注意整个函数没有 `print()` 只有返回值. 

### 为什么不用 print? 

因为 Library 应该返回结果. 

例如：`result = check_hostname(hostname)`

以后 Report Module 自己决定如何展示. 

## Step 3 — check_ntp()

Parser 返回：

```
[
    "10.1.1.1"
]
```

或者：[]

Compliance 判断：

```python
def check_ntp(ntp_servers):
    return len(ntp_servers) > 0
```

这里 Compliance 完全不知道 Cisco CLI. 只知道 Python List. 

## Step 4 — check_logging()

Parser 返回 True 或者 False

Compliance 甚至可以直接：

```python
def check_logging(logging_enabled):
    return logging_enabled
```

这也是 Parser：提前处理数据带来的好处. 

## Step 5 — check_ssh()

Parser 返回 "2" 或者 "1"

Compliance 判断：

```python
def check_ssh(ssh_version):
    return ssh_version == "2"
```

这里 Enterprise Baseline 终于体现出来. 如果以后企业修改 Baseline. 例如要求 Version X 只修改 Compliance. Parser 完全不用动. 

## Step 6 — check_password_encryption()

Parser 返回 True 或者 False

Compliance：

```python
def check_password_encryption(enabled):
    return enabled
```

保持统一风格. 

## 为什么每条 Rule 都独立? 

假设以后企业新增 SNMP, 只需要增加 `def check_snmp(...):` 其它所有 Rule 不用改. 

整个 Framework 保持稳定. 

## Rule 不应该互相调用

例如不要：

```python
def check_hostname(...):

    ...

    check_ntp(...)
```

或者：

```python
def check_logging(...):

    if check_hostname(...):

        ...
```

为什么? 因为 Compliance 应该一次发现所有问题, 而不是前一个失败, 后面全部停止. 

## Compliance Result

随着 Rule 越来越多, 需要统一返回格式. 

### 第一版保持简单. 

例如：

```python
{
    "Hostname": True,
    "Banner": True,
    "Logging": False,
    "NTP": True,
    "SSH": True,
    "Password Encryption": True
}
```

注意这里只是数据. 不是最终 Report. 

### 为什么不用 List? 

例如不要：

```python
[
    True,
    False,
    True
]
```

因为以后根本不知道第二个对应哪个 Rule. 使用字典更加清晰. 

## 一个完整流程

Parser 得到：

```python
hostname = "R1"

ntp_servers = []

ssh_version = "2"

logging_enabled = True

password_encryption = True
```

Compliance 得到：

```python
results = {
    "Hostname": check_hostname(hostname),
    "NTP": check_ntp(ntp_servers),
    "SSH": check_ssh(ssh_version),
    "Logging": check_logging(logging_enabled),
    "Password Encryption": check_password_encryption(password_encryption),
}
```

最终返回：

```python
{
    "Hostname": True,
    "NTP": False,
    "SSH": True,
    "Logging": True,
    "Password Encryption": True
}
```

整个模块没有任何输出. 

## 为什么这是 Library? 

因为以后 CLI 可以调用, GUI 可以调用, Web 可以调用, Report 可以调用. 

所有 Workflow 共享同一套 Business Logic. 

## Engineering Checklist

完成本实验后, 应确认：

| 检查项                           | 状态 |
| ----------------------------- | -- |
| `compliance.py` 不建立 SSH       | ✅  |
| `compliance.py` 不读取配置文件       | ✅  |
| `compliance.py` 不解析 Cisco CLI | ✅  |
| 每条 Rule 独立                    | ✅  |
| 所有 Rule 返回布尔值                 | ✅  |
| 使用 Dictionary 保存结果            | ✅  |

## 优化

随着 Rule 数量增加, 继续增加：

```python
check_hostname()
check_ntp()
check_logging()
...
```

会让调用代码越来越长. 

一种更具扩展性的设计是把 Rule 放到一个集合中统一执行, 例如：

```python
rules = [
    ("Hostname", check_hostname, hostname),
    ("NTP", check_ntp, ntp_servers),
    ("SSH", check_ssh, ssh_version),
]
```

然后循环执行, 自动生成结果字典. 

不过, 这会引入函数作为对象（First-Class Functions）等新的 Python 设计思想. 为了保持与前面章节一致的学习节奏, 本章仍采用显式调用每条 Rule 的方式, 等后续 Workbook 的 Python 能力进一步扩展后, 再逐步演进 Framework. 

在 Lab 9.2 中说到了对 Parser 的拆分, 在 Compliance 中也是如此, 在生产环境中随着业务需求增加也会对应增加例如

```python
check_ospf()

check_bgp()

check_vrf()

check_qos()
...
```

同样会进行拆分

```
compliance/

    system.py
    routing.py
    security.py
    services.py
```

```python
def has_hostname(hostname):
    return hostname is not None

def has_ntp_servers(ntp_servers):
    return len(ntp_servers) > 0

def has_logging(logging_servers):
    return len(logging_servers) > 0

def is_ssh_version_2(ssh_version):
    return ssh_version == "2"

def is_password_encryption_enabled(enabled):
    return enabled
```