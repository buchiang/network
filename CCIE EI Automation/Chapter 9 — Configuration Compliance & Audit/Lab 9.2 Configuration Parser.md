在 Lab 9.1 中，我们已经能够成功完成: 

```
Device
    │
    ▼
show running-config
    │
    ▼
backups/R1.cfg
```

现在，我们要解决下一个问题如何从 R1.cfg 中提取我们需要的信息? 

## Lab Objective

本实验的目标不是检查 Compliance. 

而是建立一个可以重复使用的 Parser Library. 

最终实现: 

```
Configuration File

        │
        ▼

Parser

        │
        ▼

Python Data

        │
        ▼

Compliance
```

注意 Parser 永远不会输出 PASS, FAIL

## 为什么需要 Parser? 

假设 R1.cfg: 

```
hostname R1

service password-encryption

ip ssh version 2

logging buffered 100000

ntp server 10.1.1.1

banner motd ^
Authorized Access Only
^
```

如果 没有 Parser, 每个 Rule 都会自己打开文件, 自己搜索 `if "hostname" in config:` 以后几十条 Rule 全部重复, 这是重复代码（Duplicate Code）. 

## Parser Workflow

整个流程: 

```
R1.cfg

     │
     ▼

Read File

     │
     ▼

Extract Information

     │
     ▼

Return Python Objects
```

注意 Parser 返回 Python 数据, 不是 Cisco CLI. 

## Step 1 — 创建 parser.py

新增: 

```
modules/

    parser.py
```

保持 Chapter 8 相同工程风格. 

## Step 2 — load_configuration()

第一件事情读取配置文件. 

输入: backup_file

输出: configuration

例如: 

```python
from pathlib import Path


def load_configuration(file_path):
    with open(file_path) as file:
        return file.read()
```

现在 Parser 已经能够读取 `backups/R1.cfg`

### 为什么先读取整个文件? 

不要每次都 open(...)

例如: 

```
check_hostname()
↓
open()

----------------

check_ntp()
↓
open()

----------------

check_banner()
↓
open()
```

这意味着同一个文件被打开很多次. 

更合理 `configuration = load_configuration(...)`

然后所有 Parser 共享这一份字符串. 

## Step 3 — get_hostname()

我们的第一个 Parser. 

输入: configuration

输出: "R1"

而不是: hostname R1

为什么? 因为 Compliance 不需要 Cisco CLI, 只需要真正的数据. 

逻辑可以描述为: 

读取每一行 ➡ 找到 hostname ➡ 返回第二个字段

例如配置: hostname R1

返回: R1

如果没有 Hostname, 返回 None, 不要返回 `"Hostname not found"`

Library 应该返回数据, 不是错误信息. 

## Step 4 — get_ntp_servers()

第二个 Parser. 

配置: 

```
ntp server 10.1.1.1

ntp server 10.1.1.2
```

Parser 应该返回: 

```
[
    "10.1.1.1",
    "10.1.1.2"
]
```

而不是 `ntp server ...` 为什么? 

因为以后 Compliance 只关心有没有 Server, 或者 Server 数量. 

如果没有 NTP, 返回 [], 不是 None

为什么? 

因为这里代表找到零个, 不是发生错误. 

这是一个很重要的 Python API 设计细节: 

- 没有找到任何 NTP Server → 返回空列表 []

- 解析失败或发生异常 → 才考虑抛出异常或由上层处理

## Step 5 — get_ssh_version()

配置: ip ssh version 2

返回: "2"

没有返回: None

## Step 6 — get_logging()

配置: logging buffered 100000

返回: True

没有返回: False

为什么? 

因为这里只需要回答一个问题是否配置了 Logging? 以后如果企业需要 Buffer Size 再升级. 

## Step 7 — get_password_encryption()

配置 service password-encryption

返回: True

否则: False

依然只返回: Python 数据. 

## Parser 不应该知道 Baseline

例如 Parser 返回: ssh_version = "1" 或者 ssh_version = "2"

它不知道企业要求 Version 2, 这是 Compliance 负责. 

如果 Parser 开始判断: 

```python
if version == "2":

    PASS
```

那么 Parser 已经违反职责分离. 

## Parser 的统一风格

整个 Parser 建议保持一致. 

例如: 

| Function                  | Return     |
| ------------------------- | ---------- |
| get_hostname()            | str / None |
| get_ssh_version()         | str / None |
| get_ntp_servers()         | list       |
| get_logging()             | bool       |
| get_password_encryption() | bool       |


注意相同类型保持一致. 

例如不要: get_logging() ➡ "Enabled"

另一边: get_password() ➡ True

统一 API, 以后最好维护. 

## 工程检查（Engineering Checklist）

完成本 Lab 后，应确认: 

| 检查项                         | 状态 |
| --------------------------- | -- |
| `parser.py` 不建立 SSH         | ✅  |
| `parser.py` 不打开网络连接         | ✅  |
| `parser.py` 不输出 PASS / FAIL | ✅  |
| Parser 只负责提取数据              | ✅  |
| 返回 Python 数据，而不是打印文本        | ✅  |
| 各函数返回类型保持一致                 | ✅  |

```python
from pathlib import Path

def load_configuration(file_path):
    """Load a configuration file and return it as a string."""
    with open(file_path) as file:
        return file.read()


def get_hostname(config):
    """Return the configured hostname."""
    for line in config.splitlines():
        line = line.strip()

        if line.startswith("hostname "):
            return line.split()[1]

    return None


def get_ntp_servers(config):
    """Return a list of configured NTP servers."""
    ntp_servers = []

    for line in config.splitlines():
        line = line.strip()

        if line.startswith("ntp server "):
            ntp_servers.append(line.split()[2])

    return ntp_servers


def get_logging(config):
    """Return a list of configured syslog servers."""
    logging_servers = []

    for line in config.splitlines():
        line = line.strip()

        if line.startswith("logging host "):
            logging_servers.append(line.split()[2])

    return logging_servers


def get_ssh_version(config):
    """Return the configured SSH version."""
    for line in config.splitlines():
        line = line.strip()

        if line.startswith("ip ssh version "):
            return line.split()[3]

    return None


def get_password_encryption(config):
    """Return True if service password-encryption is enabled."""
    for line in config.splitlines():
        line = line.strip()

        if line == "service password-encryption":
            return True

    return False


def parse_configuration(config):
    """Parse the running configuration into a structured dictionary."""
    return {
        "hostname": get_hostname(config),
        "ntp_servers": get_ntp_servers(config),
        "logging_servers": get_logging(config),
        "ssh_version": get_ssh_version(config),
        "password_encryption": get_password_encryption(config),
    }
```

在 parser.py 里做的都是字符串搜索, 负责提取数据, 另一种方式让 Rule 自己解析

现在返回的结果都是 bool 只有 True 和 False, 在真实生产环境中并不会这样, 生产环境中涉及到 数据模型 Data Model

随着 Parser 越来越大,企业通常会继续拆分.

例如:

```
parser/

    system.py
    interface.py
    routing.py
    security.py
```

而不是 parser.py 但是目前 Chapter 9 保持 parser.py 即可.

等 Framework 成长再拆分,这一点非常符合企业的发展过程.