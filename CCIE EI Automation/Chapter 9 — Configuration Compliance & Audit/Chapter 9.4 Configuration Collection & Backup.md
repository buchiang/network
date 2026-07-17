到目前为止, 我们已经建立了: 

- Enterprise Baseline

- Compliance Rule

- Desired State

- Configuration Drift

现在终于可以开始真正的 Compliance Workflow. 

## Compliance 的第一步

很多初学者认为第一步应该是 Compare Configuration 其实不是. 真正的第一步永远都是 Collect Configuration 因为如果没有设备当前配置, 根本无法比较. 

所以整个 Workflow 应该变成: 

```
Device

    │
    ▼

Collect Running Configuration

    │
    ▼

Save Backup

    │
    ▼

Compliance Check

    │
    ▼

Audit Report
```

注意 Collect 和 Compliance 是两个不同阶段. 

## 为什么要先采集？

假设企业有500台 Router 每天凌晨执行 Compliance. 如果每检查一条 Rule 都执行 `show running-config` 

例如: 

第一条 Rule: Hostname, 执行一次 SSH. 

第二条: Logging, 再执行一次. 

第三条: Banner, 再执行一次. 

......

最后 20 Rules × 500 Devices = 10000 SSH Commands, 其中绝大部分都是重复获取同一份配置, 企业不会这样做. 

而是: 

Collect Once ➡ Store Once ➡ Analyze Many Times

这是 Enterprise Automation 中非常重要的设计原则. 

## Backup 的职责

因此我们新增 

```
modules/

    backup.py
```

它只有一个职责负责采集并保存设备配置. 

它不负责

- Compliance

- Parsing

- Report

- Deployment

这仍然遵循前几章建立的单一职责原则(Single Responsibility Principle). 

## Backup Workflow

对于每台设备执行: 

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

Receive Output

    │
    ▼

Write File
```

最终生成

```
backups/

    R1.cfg
    R2.cfg
    R3.cfg
```

以后所有模块统一读取这里. 

## 为什么保存文件？

很多人会问为什么不直接 `running_config = connection.send_command(...)` 然后一直放在内存里面？

当然可以, 但是企业通常不会这样原因有很多. 

### 原因一: 保留历史记录

今天 `R1.cfg`, 明天再次采集 `R1.cfg`, 后天继续采集. 

如果保存历史, 以后就可以比较 Monday ➡ Tuesday ➡ Wednesday 配置到底哪里变了. 

虽然本章不会实现历史版本管理, 但**保留配置快照(Snapshot)**是很多企业的基础实践. 

### 原因二: 方便离线分析

例如晚上统一采集所有设备. 

白天 Compliance Server 直接分析 `.cfg` 无需再次连接设备. 

这样可以减少 SSH Session. 

### 原因三: 方便 Debug

假设 Compliance 报告 FAIL, 工程师第一件事情就是打开 `R2.cfg` 查看真正配置. 

如果没有 Backup 很多问题无法重现. 

## Backup 目录

保持工程一致性, 新增: 

```
automation_project/

    backups/

        R1.cfg

        R2.cfg

        R3.cfg
```

注意这里保存的是 Running Configuration Snapshot. 不是 Startup Config. 

因为 Compliance 关注的是设备当前真正运行的配置. 

## 为什么不是 Startup Configuration？

Cisco 两个配置 Running Configuration, Startup Configuration

Running 当前正在工作. 

Startup 重启才加载. 

例如工程师刚执行 `hostname R1`, 但是忘记 `write memory` 

于是 Running: `hostname R1`

Startup: `hostname Router`

企业真正关心的是用户现在访问的设备. 因此 Compliance 检查 Running Configuration. 

## Backup 是否会修改设备？

不会, 整个 Backup 只有 `show running-config` 属于 Read Only. 不会 `configure terminal` 不会 `copy running startup` 不会 `reload` 因此 Backup 属于 **Non-Intrusive Operation(非侵入式操作)**. 

这是企业普遍要求的重要原则: 

>Audit 不应改变设备状态. 

## Backup 是整个 Audit 的基础

以后 Compliance 读取 R1.cfg

Parser 读取 R1.cfg

Diff 读取 R1.cfg

Report 读取 R1.cfg

所有模块共享同一个输入. 

这也是前面提到的: 

Collect Once ➡ Analyze Many Times

## 与 Chapter 8 的集成

我们已经有: 

```
modules/

    connection.py
```

因此 Backup 不会重新实现 SSH. 而是直接调用 `connection = create_connection(device)` 然后执行: 

```python
connection.send_command(
    "show running-config"
)
```

最后写入 `backups/R1.cfg` 这样整个项目继续保持模块复用. 

## 第一版 Backup 模块职责

目前 backup.py 仅提供三个功能. 

Connect Device ➡ Collect Running Config ➡ Save File

除此之外什么都不做. 

例如不会

- Compliance

- Diff

- Parse

- Report

- Remediation

因为每个模块只负责一件事情. 

## 一个容易犯的错误

很多初学者喜欢写这样的函数: 

```python
backup_and_check_and_report()
```

函数里面: 

- SSH

- 获取配置

- 比较

- 打印结果

- 写日志

- 导出报告

全部混在一起. 

这种设计在几十行代码时看起来很方便, 但随着功能增加, 很快就会变得难以维护和测试. 

相比之下 backup.py ➡ parser.py ➡ compliance.py ➡ report.py 每个模块独立. 

未来任何一个模块都可以单独测试. 这正是企业工程化代码与一次性脚本的重要区别. 

## 本节总结

本节完成了 Compliance Workflow 的第一步设计: 

- Collect Configuration 永远先于 Compare. 

- backup.py 的职责仅限于采集并保存 Running Configuration. 

- Compliance, Parser, Report 等模块共享同一份配置快照, 实现 Collect Once, Analyze Many Times. 

- Audit 使用 Running Configuration, 因为它反映设备的实时状态. 

- Backup 是只读(Read Only), 非侵入式(Non-Intrusive)的操作, 不会修改设备配置. 