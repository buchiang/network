上一节介绍了 Automation Pipeline 的概念. 

本节将进一步回答一个工程设计问题: 一个企业级网络自动化项目应该按照什么顺序执行? 

在实验环境中，我们通常直接运行一个脚本: python deploy.py 脚本完成所有工作, 但在企业环境中，自动化任务通常被拆分为多个固定阶段，每个阶段都有明确的输入, 输出和职责. 

## Pipeline 的设计原则

一个优秀的 Pipeline 应满足以下原则: 

1. 顺序明确(Sequential)

每个 Stage 都有固定的执行顺序. 

例如: Inventory ➡ Render ➡ Deploy ➡ Validate

不能跳过某一步. 

例如: 不能在没有生成配置的情况下直接部署. 

2. 输入和输出固定(Well-defined Input/Output)

每个 Stage 只关心自己的输入. 

例如: 

#### Inventory Stage

输入: devices.json

输出: devices

#### Render Stage

输入: devices 以及: hostname.j2

输出: R1.cfg, R2.cfg, R3.cfg

Render Stage 不需要知道配置如何部署. 

### Deploy Stage

输入: R1.cfg, R2.cfg

输出: Deployment Result

Deploy Stage 不需要重新生成配置. 

3. 职责独立(Independent Responsibilities)

每个 Stage 只负责一件事情. 

例如: 

Inventory Stage: 负责读取数据. 

Render Stage: 负责生成配置. 

Deploy Stage: 负责 SSH. 

Validation Stage: 负责验证. 

不要让任何一个 Stage 同时承担多个职责. 

## 一个典型的 Enterprise Pipeline

企业自动化通常可以抽象为下面几个阶段: 

```
             Inventory
                 │
                 ▼
          Load Device Data
                 │
                 ▼
          Validate Inventory
                 │
                 ▼
        Render Configuration
                 │
                 ▼
         Save Rendered Files
                 │
                 ▼
             Dry Run
                 │
                 ▼
             Deployment
                 │
                 ▼
          Configuration Check
                 │
                 ▼
         Archive & Logging
```

下面逐一分析每个阶段. 

### Stage 1 — Load Inventory

职责: 读取所有设备信息. 

例如: devices.json

加载为: devices

输出的数据对象将提供给后续所有 Stage. 

这一阶段只负责读取数据, 不进行配置生成, 不连接设备. 

### Stage 2 — Validate Inventory

读取数据之后，应立即进行基本检查. 

例如: 检查是否存在 hostname, management_ip, username, password, platform

如果 Inventory 本身存在错误，整个 Pipeline 应立即停止, 而不是继续执行. 

这样可以避免几十台设备已经开始部署，才发现第 35 台设备缺少 IP 地址. 越早发现错误，修复成本越低. 

### tage 3 — Render Configuration

这一阶段调用: Jinja2

例如: hostname.j2, device

得到: 

```
hostname R1

interface Loopback0

 ip address 1.1.1.1
```

此时: 配置仅存在于本地, 设备没有任何变化. 

### Stage 4 — Save Rendered Files

很多初学者喜欢 Render 后直接 `send_config_set()` 企业通常不会这样做. 

而是先保存: 

```
output/

    R1.cfg
    R2.cfg
    R3.cfg
```

这样做有几个好处. 

#### 好处一

方便人工 Review, 网络工程师可以打开 R1.cfg 检查有没有错误. 

#### 好处二

方便比较, 例如 Git Diff 可以看到昨天 hostname R1 今天 hostname R2 所有修改都可以追踪. 

#### 好处三

方便审计(Audit), 很多企业要求所有部署配置必须保存. 以后可以追溯是谁生成的? 什么时候生成? 配置内容是什么? 

### Stage 5 — Dry Run

Dry Run: 模拟执行. 

特点不会修改设备. 

例如输出: 

```
========== DEVICE ==========
R1

========== CONFIG ==========
hostname R1

interface Loopback0

 ip address 1.1.1.1
```

然后结束程序, 整个部署过程到此为止. 

Dry Run 是企业自动化中降低风险的重要机制，尤其适用于大规模变更前的检查. 

### Stage 6 — Deployment

只有经过前面阶段的检查之后，才真正开始: SSH ➡ Netmiko ➡ `send_config_set()`

部署完成后，记录成功, 失败, 失败原因, 耗时, 日志. 这一阶段只负责部署, 不要重新 Render, 不要重新读取 Inventory. 

### Stage 7 — Validation

部署成功并不代表配置已经生效. 因此需要再次执行 `show running-config` 或者 `show ip interface brief` 验证设备是否已经达到预期状态. 

Validation 是自动化流程中不可缺少的一环，它验证的是结果而不是过程. 

### Stage 8 — Archive

最后保存日志, 配置, 输出结果, 错误信息

例如: 

```
logs/

deployment.log

output/

R1.cfg
R2.cfg
R3.cfg
```

这样整个 Pipeline 完整结束. 

## 为什么要拆成这么多 Stage? 

因为企业真正维护的是长期运行的系统. 而不是一次性的脚本. 

例如未来需要增加审批(Approval)可以直接: Render ➡ Approval ➡ Deploy

增加回滚: Deploy ➡ Rollback

增加通知: Deploy ➡ Email Report

由于各个 Stage 的职责已经清晰划分，只需插入新的 Stage，而不需要重写整个程序. 这正是 Pipeline 设计的价值所在. 

## 本节小结

本节设计了一个完整的企业级 Automation Pipeline，并明确了各阶段的职责: 

1. Load Inventory: 读取设备数据. 

2. Validate Inventory: 检查 Inventory 的完整性和合法性. 

3. Render Configuration: 使用 Jinja2 渲染配置. 

4. Save Rendered Files: 保存生成的配置，便于 Review, 审计和版本管理. 

5. Dry Run: 模拟执行，不修改设备. 

6. Deployment: 通过 Netmiko 将配置下发到设备. 

7. Validation: 验证设备是否达到预期状态. 

8. Archive: 保存日志, 配置和执行结果. 

从下一节开始，我们将按照这一 Pipeline，逐步实现一个具有企业工程结构的自动化项目. 整个实现仍然基于 SSH 和前七章的知识，不会引入 Chapter 9 及之后的 API 或自动化框架内容. 