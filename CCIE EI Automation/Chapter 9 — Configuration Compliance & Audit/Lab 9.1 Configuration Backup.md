在理论部分, 我们设计了 backup.py, 现在开始真正实现它. 

本 Lab 的目标只有一个将设备的 Running Configuration 保存到本地文件. 

除此之外: 

- 不做 Compliance

- 不做 Parser

- 不做 Report

坚持 Single Responsibility Principle. 

Lab Objective 最终实现: 

```
Inventory

      │
      ▼

SSH Connection

      │
      ▼

show running-config

      │
      ▼

Save Configuration

      │
      ▼

backups/R1.cfg
```

## Step 1 — 创建目录

在项目中新增: 

```
automation_project/

├── backups/
```

用于保存每台设备的配置快照. 

例如: 

```
backups/

    R1.cfg
    R2.cfg
    R3.cfg
```

## Step 2 — 创建 backup.py

新增: 

```
modules/

    backup.py
```

[backup.py](Lab/modules/backup.py) 这个模块只负责: 

- 获取 Running Configuration

- 保存文件

## Step 3 — 设计函数

保持 Chapter 8 的工程风格, 不要写 `backup_everything()` 而是职责明确: 

```python
get_running_configuration()

save_backup()
```

这样以后任何 Workflow 都可以复用. 

`get_running_configuration()`

输入: connection

输出: running_config

逻辑: 

```python
def get_running_configuration(connection):
    return connection.send_command("show running-config")
```

这里只负责获取配置, 不保存. 

`save_backup()`

输入: hostname, configuration

输出: `backups/R1.cfg`

例如: 

```python
from pathlib import Path

def save_backup(hostname, configuration):
    backup_directory = Path("backups")
    backup_directory.mkdir(exist_ok=True)

    backup_file = backup_directory / f"{hostname}.cfg"

    with open(backup_file, "w") as file:
        file.write(configuration)

    return backup_file
```
这里使用 pathlib 而不是字符串拼接路径, 是因为它具有更好的可移植性和可读性, 也是现代 Python 工程中更常见的写法. 

为什么拆成两个函数? 

很多新人会写: 

```python
def backup():

    show running-config

    write file
```

虽然能工作, 但是以后如果想只获取配置怎么办? 

例如: 

Parser 可能直接需要 `config = get_running_configuration(connection)`

而不是立即写文件, 所以拆分职责以后更容易复用. 

## Step 4 — 创建 Workflow

在: 

```
scripts/

    compliance.py
```

里面. 

第一版 Workflow 只有: 

Load Inventory ➡ Connect Device ➡ Get Running Configuration ➡ Save Backup

暂时不要加入 Parser. 

## Workflow 伪代码

```
for each device

        │
        ▼

connect

        │
        ▼

collect configuration

        │
        ▼

save backup

        │
        ▼

disconnect
```

是不是发现和 Chapter 8 Deployment Workflow 非常相似. 只是最后一步不是 Deploy 而是 Backup

## 预期结果

假设 Inventory 有三台设备, 运行 `python3 -m scripts.compliance`

最终应该得到: 

```
automation_project/

backups/

    R1.cfg

    R2.cfg

    R3.cfg
```

打开 R1.cfg 应该看到:

```
hostname R1

service password-encryption

ip ssh version 2

logging buffered 100000

ntp server 10.1.1.1

...
```

说明第一阶段成功. 

## 工程检查(Engineering Checklist)

完成本 Lab 后, 应确认以下几点: 

| 检查项                         | 状态 |
| --------------------------- | -- |
| `backup.py` 不负责 Compliance  | ✅  |
| `backup.py` 不负责 Parser      | ✅  |
| 配置保存在 `backups/`            | ✅  |
| 每台设备生成独立 `.cfg` 文件          | ✅  |
| 使用已有 `connection.py` 建立 SSH | ✅  |
| Workflow 与 Chapter 8 保持一致   | ✅  |

```python
from pathlib import Path

def get_running_configuration(connection):
    return connection.send_command("show running-config")

def save_backup(hostname, configuration):
    backup_directory = Path("backups")
    backup_directory.mkdir(exist_ok=True)

    backup_file = backup_directory / f"{hostname}.cfg"

    with open(backup_file, "w") as file:
        file.write(configuration)

    return backup_file
```

其实在 Chapter 8 里的 output.py 已经能实现保存 configuration 功能

```python
def save_configuration(file_path, configuration):
    """
    Save the rendered configuration to a file.

    Args:
        file_path (str): Output file path.
        configuration (str): Rendered configuration.
    """

    try:
        with open(file_path, 'w') as file:
            file.write(configuration)
    
    except Exception as e:
        print(f"Failed to save configuration: {e}")
        raise
```