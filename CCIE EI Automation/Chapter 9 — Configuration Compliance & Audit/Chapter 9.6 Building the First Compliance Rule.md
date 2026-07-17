经过前面的设计, 现在终于来到本章最重要的一步: 

>编写第一条真正的 Compliance Rule. 

到目前为止, 我们已经拥有: 

connection.py ➡ backup.py ➡ parser.py

现在新增: compliance.py

整个 Compliance Framework 开始真正运行. 

## Compliance Rule 的职责

先回顾各模块的职责. 

connection.py 负责SSH Connection

backup.py 负责 Collect Running Configuration ➡ Save Configuration

parser.py 负责 Extract Information

例如 `hostname = get_hostname(config)`


### compliance.py

终于开始 Evaluate ➡ PASS / FAIL

注意只有 compliance.py 才有资格决定 PASS, FAIL 其它模块都不能. 

## 第一条 Rule

按照上一节建立的 Enterprise Baseline. 

我们先选择最简单的一条 `Hostname 必须存在` 为什么? 

因为它几乎没有业务逻辑, 适合理解整个 Framework. 

### Rule 的思考过程

企业标准 Hostname 必须存在 Parser 返回 `hostname = "R1"` Compliance 只需要判断 `if hostname` 即可. 

如果 `hostname = None` 说明没有 Hostname. 

结果 FAIL

### Compliance 的输入

这里非常重要, Compliance 不应该自己打开 R1.cfg 也不应该自己搜索 hostname 而应该接受 Parser 已经解析好的数据. 

例如: 

```python
hostname = parser.get_hostname(config)

check_hostname(hostname)
```

这样 Compliance 完全不知道 Cisco Configuration 长什么样. 

### 第一版 check_hostname()

整个函数可以抽象成: 

```python
def check_hostname(hostname):

    if hostname:
        return True

    return False
```

注意这里没有 `print()` 没有 `logging` 没有 SSH 只有 Business Logic. 

### 为什么返回 True / False? 

因为 Library 应该返回结果. 

例如: 

`result = check_hostname(hostname)`

然后 Report Module 决定如何展示. 

例如 Hostname ........ PASS

或者 Hostname ........ FAIL

如果 Compliance 自己打印. 以后 Report 几乎无法重用. 

## 第二条 Rule

接下来 NTP. 

Enterprise Baseline 规定至少存在一个 ntp server

Parser 提供 ntp_servers

例如: 

```
[
    "10.1.1.1"
]
```

或者 `[]`

Compliance 判断 `if ntp_servers` PASS. 

否则 FAIL. 

注意 Compliance 根本不知道配置是不是 `ntp server 10.1.1.1` 还是 `ntp server 192.168.1.10 prefer` Parser 已经处理了. 

## 第三条 Rule

SSH

Baseline `ip ssh version 2`

Parser 返回 `ssh_version`

例如 `"2"`

Compliance 判断 `ssh_version == "2"` PASS. 

否则 FAIL. 

每条 Rule 都应该独立

不要: 

```python
def compliance_check():

    check_hostname()

    check_ntp()

    check_banner()

    check_logging()

    check_ssh()
```

全部混在一起. 

更好的设计: 

```python
check_hostname()

check_ntp()

check_banner()

check_logging()

check_ssh()
```

每一个都是独立函数. 这样以后新增 `check_snmp()` 无需修改已有代码. 继续符合 Open-Closed Principle. 

## Rule 应该简单

很多新人喜欢把很多事情放进一条 Rule. 

例如: 

Hostname 必须 R1, 同时必须开启 SSH, 同时必须配置 NTP

这是错误设计. Rule 应该只回答一个问题. 

例如: 

Hostname 是否存在? 

回答 PASS, FAIL

结束. 

下一条 Rule SSH 是否 Version 2? 

再回答 PASS, FAIL

Rule 越简单, 整个系统越容易维护. 

## Rule 与 Rule 之间不能互相依赖

例如不要: 

```python
if check_hostname():

    check_ntp()
```

为什么? 因为如果 Hostname 失败. NTP 永远不会检查. 

最终 Report 变成: 

Hostname ...... FAIL

NTP ........... 未检查

SSH ........... 未检查

企业最需要的是一次看到所有问题. 因此正确方式: 

```
Hostname
↓
----------------
PASS/FAIL
----------------

NTP
↓
----------------
PASS/FAIL
----------------

SSH
↓
----------------
PASS/FAIL
----------------
```

每条完全独立. 

## Compliance Result

随着 Rule 增加, 最终形成统一 Compliance Result. 

例如: 

```
Device: R1

Hostname ........ PASS

Banner .......... PASS

Logging ......... PASS

NTP ............. FAIL

SSH ............. PASS

Encryption ...... PASS
```

这里已经开始出现 Report 的雏形, 但是注意目前 Compliance 仍然只负责判断. Report 属于下一节. 

## 与 Chapter 8 的联系

可以看到 Chapter 8 建立的是 Deployment Framework. 

Inventory ➡ Render ➡ Deploy

Chapter 9 建立的是 Audit Framework. 

Inventory ➡ Backup ➡ Parser ➡ Compliance ➡ Report

两条 Workflow互相独立, 但是共享同一个工程结构. 

这正是企业自动化平台常见的设计方式: Deployment 与 Audit 是两个独立工作流, 它们共享 Inventory, Connection, Logging 等基础模块, 而不是彼此耦合. 

## 本节总结

本节完成了第一条 Compliance Rule 的设计: 

- compliance.py 是唯一负责 PASS / FAIL 判断的模块. 

- 每条 Compliance Rule 只检查一个目标, 保持单一职责. 

- Compliance 基于 Parser 返回的数据, 而不是直接解析配置文件. 

- 每条 Rule 相互独立, 避免级联依赖, 确保一次检查能够发现所有问题. 

- Compliance 返回判断结果, Report 再负责统一展示. 