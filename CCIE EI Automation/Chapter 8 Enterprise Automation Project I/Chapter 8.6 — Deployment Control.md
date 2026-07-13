前面的章节已经完成了: 

- Pipeline

- Project Structure

- Dry Run

现在开始真正进入 Deployment(部署)但是企业真正关心的问题并不是如何发送配置? 而是如何安全地发送配置? 这就是: 

>Deployment Control(部署控制)

## 为什么需要 Deployment Control? 

实验环境通常只有: R1, R2, R3, 直接: 

```
for device in devices:

    deploy(device)
```

几秒钟结束, 但是企业可能有120 Core Devices, 450 Distribution Switches, 3200 Access Switches如果第5台设备失败, 后面的3700台设备是否继续? 这就不是 Netmiko 能解决的问题, 而是 Deployment Strategy. 

## Deployment 不只是发送配置

很多初学者理解 Deployment 就是 `send_config_set()` 实际上企业中的 Deployment Stage 通常包含: 

Select Device ➡ Connect ➡ Deploy Configuration ➡ Check Result ➡ Record Status ➡ Disconnect

注意真正发送配置, 只是其中一步. 

## 每台设备都应该拥有独立状态

企业自动化不会只有成功, 失败, 两个状态. 通常每台设备都会维护自己的部署状态. 

例如: 

R1(Pending)  ➡ R1(Deploying) ➡ R1(Success) 或者 R1(Failed)

这样个项目可以知道哪些设备已经完成. 哪些仍在等待. 

```
Device        Status

R1            Success

R2            Success

R3            Failed

R4            Pending
```

即使 R3 失败, 仍然能够清楚看到整个部署进度. 

## Fail Fast 与 Continue

企业通常存在两种部署策略. 

### Strategy 1: Fail Fast

R1(Success) ➡ R2(Failed) ➡ STOP

发现错误立即停止. 后面的设备全部取消. 这种策略适用于: 

- Core Router

- Internet Edge

- Data Center Gateway

因为这些设备的重要性非常高. 任何错误, 都可能影响整个网络. 

### Strategy 2: Continue

R1(Success) ➡ R2(Failed) ➡ R3(Success) ➡ R4(Success)

即使某台设备失败, 整个任务继续执行. 最后统一生成失败列表. 这种策略更适用于 Access Layer. 

例如部署1000台 Access Switch 其中2台失败, 没有必要停止整个部署. 

## 为什么不要因为一台设备中断整个程序? 

错误设计: 

R1(Success) ➡ R2(SSH Timeout) ➡ Program Crash

这样程序结束, 不知道还有多少设备没有部署. 

正确设计: 

R1(Success) ➡ R2(SSH Timeout) ➡ Record Failure ➡ Continue

最后输出 

```
Deployment Summary

Success: 98

Failed: 2
```

这也是前面 Chapter 4 中讨论的异常隔离(Exception Isolation). 每台设备的异常, 应尽量限制在当前设备范围内, 不要影响整个 Pipeline. 

## Deployment Summary

企业自动化几乎都会生成部署摘要. 

例如: 

```
====================================

Deployment Summary

====================================

Total Devices : 20

Successful    : 18

Failed        : 2

Skipped       : 0

====================================
```

如果存在失败设备继续输出: 

```
Failed Devices

--------------

R3

SSH Authentication Failed

R17

Connection Timeout
```

这样工程师无需翻阅日志, 即可快速了解整体情况. 

## 为什么 Summary 比日志更重要? 

日志(Log)适合排查问题. 

例如: 

```
09:15:31 Connecting R3

09:15:34 Authentication Failed
```

但是管理者通常更关心 

```
Today

200 Devices

198 Success

2 Failed
```

因此 Summary 回答的是发生了什么. 而 Log 回答的是为什么发生. 二者缺一不可. 

## Deployment 应保持可预测(Predictable)

企业自动化非常强调: 

>可预测性(Predictability)

例如 Inventory R1, R2, R3, R4 部署每次都应该按照: 

R1 ➡ R2 ➡ R3 ➡ R4

不要 R2 ➡ R1 ➡ R4 ➡ R3

因为这会增加排查问题的难度. 保持固定执行顺序, 可以提高可重复性(Repeatability). 

## Deployment 与 Rollback

Deployment Stage 不仅需要考虑成功. 还要考虑失败. 因此部署前通常已经完成 `Backup Running Configuration` 如果部署失败, 至少具备恢复原始配置的基础. 

需要说明的是本章只讨论为回滚做好准备. 真正的 Rollback Strategy 将在后续章节中进行更系统的设计, 本章不会提前展开实现细节. 

## 工程经验

企业部署最重要的目标不是尽快完成部署. 

而是让整个部署过程可观察(Observable), 可预测(Predictable)和可恢复(Recoverable). 

一个部署系统应该始终能够回答以下几个问题: 

- 当前正在部署哪台设备? 

- 已完成多少台设备? 

- 哪些设备失败? 

- 为什么失败? 

- 是否继续执行? 

- 是否具备恢复条件? 

如果这些问题能够快速回答, 自动化系统就更容易投入生产环境. 

## 本节小结

本节介绍了 Deployment Control 的核心设计思想: 

- Deployment 不只是发送配置, 还包括连接, 部署, 状态记录和结果汇总. 

- 每台设备应维护独立的部署状态, 避免单点失败影响整体可观测性. 

- 根据业务场景, 可以选择 Fail Fast 或 Continue 两种部署策略. 

- 使用 Deployment Summary 快速展示整体结果, 而日志用于定位具体原因. 

- 部署过程应保持固定顺序, 保证可预测性和可重复性. 

- 在部署之前应完成配置备份, 为后续可能的回滚保留恢复基础, 但本章暂不实现完整的 Rollback 流程. 

至此, Chapter 8 已经完成了企业级自动化项目从 Pipeline 设计, 工程结构, Dry Run 到 Deployment Control 的核心流程, 为下一步实现完整的企业 SSH 自动化工程奠定了统一的工程基础. 