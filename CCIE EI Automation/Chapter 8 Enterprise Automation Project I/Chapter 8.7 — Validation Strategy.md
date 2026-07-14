前面的章节已经完成了: 

- Pipeline Design

- Project Structure

- Dry Run

- Deployment Control

很多初学者认为配置已经成功发送, 自动化任务就结束了. 事实上, 对于企业网络来说: 

Deployment Success ≠ Configuration Success

能够成功执行 `send_config_set()` 只能说明设备接受了配置命令. 并不能证明网络已经达到预期状态. 

因此, 企业自动化必须增加最后一个关键阶段 Validation(验证)

## 为什么需要 Validation？

假设部署成功

```
hostname R1

interface Loopback0

 ip address 1.1.1.1 255.255.255.255
```

Netmiko 返回 `Configuration Complete` 很多人就认为部署结束. 但是实际上可能出现: 

- Interface Shutdown

- OSPF Neighbor 没有建立

- BGP Session 未建立

- VLAN 不存在

- ACL 顺序错误

- 静态路由没有安装

也就是说配置已经进入设备, 但是业务没有恢复. 

因此企业真正关心的是: 

>Desired State(期望状态)是否已经实现. 

## Validation 验证什么？

Validation 并不是重新读取配置. 而是验证设备是否已经达到目标状态. 

例如: 

如果部署的是 Loopback

应该验证 `show ip interface brief`

如果部署的是 OSPF

应该验证 `show ip ospf neighbor`

如果部署的是 BGP

应该验证 `show ip bgp summary`

如果部署的是 Static Route

应该验证 `show ip route`

重点始终是验证业务结果, 不是验证配置命令. 

## Configuration Validation 与 Service Validation

企业通常把验证分成两个层次. 

### 第一层

Configuration Validation

例如: `show running-config` 确认配置是否已经存在. 

例如: 

```
interface Loopback0

 ip address 1.1.1.1
```

已经进入 Running Configuration. 

### 第二层

Service Validation

例如: `show ip ospf neighbor`

确认 OSPF 是否建立邻居. 

或者 `show ip bgp summary`

确认 BGP 是否建立 Session. 

可以看到第二层比第一层更加重要. 因为企业最终关心的是服务, 而不是 CLI. 

## Validation 不应该修改设备

Validation 的原则非常简单只读取, 不修改. 

因此 Validation Stage 应该执行 show ... 而不是 configure terminal

Validation 是 Observation, 不是 Deployment. 

## Validation Result

每台设备最终都应该得到一个验证结果. 

例如: 

Device R1

Validation PASS

或者: 

Device R2

Validation FAIL

不要只有 Deployment Success, 因为 Deployment Success 并不表示 Validation Success. 

## Deployment 与 Validation 的关系

整个流程现在变成: 

Deploy ➡ Configuration Applied ➡ Validation ➡ PASS / FAIL

注意 Deployment 回答的是配置有没有发送？

Validation 回答的是网络有没有达到目标状态？

这是两个完全不同的问题. 

## Validation Summary

企业项目通常会输出: 

```
====================================

Validation Summary

====================================

Validated Devices : 20

Passed            : 19

Failed            : 1

====================================
```

如果失败继续输出: 

```
Validation Failed

-------------------------

R7

OSPF Neighbor Down
```

这样工程师立即知道部署已经结束, 但是业务仍然存在问题. 

## Validation 在 Pipeline 中的位置

现在整个 Pipeline 已经完整: 

Load Inventory ➡ Validate Inventory ➡ Render Templates ➡ Save Configuration ➡ Dry Run ➡ Deployment ➡ Validation ➡ Archive

注意 Validation 永远发生在 Deployment 之后. 因为只有设备已经修改, 才有验证对象. 

## 工程经验

一个成熟的自动化系统, 不应该以 Configuration Applied Successfully 作为结束. 

而应该以 Network State Verified Successfully 作为结束. 

这意味着自动化不仅负责执行变更(Execution), 还负责确认变更结果(Verification). 这也是企业自动化区别于简单脚本的重要特征. 

## 本节小结

本节建立了企业自动化中的 Validation Strategy: 

Deployment Success 不等于业务成功. 
Validation 的目标是验证 Desired State 是否实现, 而不是确认命令是否执行. 
Validation 分为 Configuration Validation 和 Service Validation 两个层次, 其中 Service Validation 更贴近企业实际需求. 
Validation 只执行读取操作, 不修改设备. 
每台设备都应产生独立的 Validation Result, 并最终汇总为 Validation Summary. 

至此, Chapter 8 的完整企业自动化流水线已经形成: 

Load Inventory ➡ Validate Inventory ➡ Render Templates ➡ Save Configuration ➡ Dry Run ➡ Deployment ➡ Validation ➡ Archive

这一 Pipeline 将作为后续章节的基础, 在保持相同工程思想的前提下, 逐步扩展到更高级的自动化技术. 