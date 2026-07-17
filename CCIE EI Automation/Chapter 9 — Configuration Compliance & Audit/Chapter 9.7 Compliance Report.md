到目前为止，我们已经完成了整个 Compliance Framework 的核心模块: 

connection.py ➡ backup.py ➡ parser.py ➡ compliance.py

可是还有一个问题. 假设我们检查了: 

- Hostname

- Banner

- Logging

- NTP

- SSH

- Password Encryption

每条 Rule 都返回 True 或者 False 那么运维工程师怎么看? 

## 企业真正需要的是 Report

Automation 最终面对的人不是 Python, 而是 Network Engineer. 

因此企业真正关心的是 `Compliance Report`

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

运维人员一眼就知道哪里出了问题. 

## 为什么不能直接 print()

很多初学者这样写

```python
print(check_hostname())

print(check_ntp())

print(check_banner())
```

最后得到

```
True

False

True

True
```

请问哪个 False? 没人知道. 所以企业不会输出 Boolean, 而是输出带有上下文的信息. 

例如: 

```
Hostname ........ PASS

NTP ............. FAIL
```

## Report 与 Compliance 的职责

这里继续坚持职责分离. Compliance 负责判断, Report 负责展示

例如 Compliance 返回: 

```python
{
    "hostname": True,
    "ntp": False,
    "banner": True
}
```

Report 决定如何显示. 

例如: 

```
Hostname ...... PASS

NTP ........... FAIL

Banner ........ PASS
```

以后如果想导出 HTML. Compliance 不用修改. 如果想导出 CSV. Compliance 仍然不用修改. 

## 为什么企业喜欢这种设计? 

因为业务逻辑不会随着输出格式改变. 

例如今天 Terminal: PASS, FAIL

明天网页: 🟢, 🔴

甚至以后发送邮件. 

Compliance 全部不用改. 

这就是 Presentation Layer(展示层)和 Business Logic(业务逻辑)分离. 

## Report 应该包含什么? 

第一版 Report 保持简单. 

建议包含: Device Name ➡ Rule Name ➡ Status

例如: 

```
================================

Compliance Report

================================

Device: R1

Hostname ........ PASS

Banner .......... PASS

Logging ......... PASS

NTP ............. FAIL

SSH ............. PASS
```

已经足够. 

## 是否需要显示原因? 

这是企业里面经常讨论的问题. 

例如 FAIL 是不是应该告诉原因? 

例如 NTP FAIL Reason: No ntp server configured.

答案应该, 但是为了保持 Workbook 渐进复杂度, 第一版先只显示 PASS, FAIL 后面再扩展. 

## 是否需要显示实际值? 

例如: SSH Baseline: Version 2

设备: Version 1

是否显示: 

```
Expected: 2

Actual: 1
```

企业通常会显示. 

例如: 

```
SSH ........ FAIL

Expected: 2

Actual: 1
```

但是第一版暂时不实现. 否则 Report 复杂度会上升很多. 

## Report 应该统一格式

不要这样: 

```
Hostname PASS

Banner PASS

Logging FAIL

SSH PASS
```

长度不一致, 可读性很差. 企业一般都会统一对齐. 

例如: 

```
Hostname ........ PASS

Banner .......... PASS

Logging ......... FAIL

NTP ............. PASS

SSH ............. PASS
```

阅读非常舒服. 

## Report 是否应该保存? 

答案应该. 不要只打印. 

例如新增: 

```
reports/

    R1_report.txt

    R2_report.txt

    R3_report.txt
```

以后审计可以查看历史 Report. 不过本章第一版仍然先输出 Terminal. 下一步再保存. 

## 一个容易犯的错误

很多新人喜欢每条 Rule 自己打印. 

例如: 

```python
def check_ntp():

    print("PASS")
```

然后 Banner 再 `print("FAIL")` 最后整个程序输出乱七八糟. 

正确流程应该: Rule ➡ Return Result ➡ Collect Results ➡ Generate Report

而不是: Rule ➡ Print

这也是为什么前一节所有 Rule 都返回 True, False. 

## Compliance Framework 的完整 Workflow

现在整个 Framework 已经完整. 

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

Compliance Rules

        │
        ▼

Collect Results

        │
        ▼

Compliance Report
```

这就是 Chapter 9 最大的目标. 

## 一个企业中的典型运行流程

每天凌晨 Automation Server 执行: 

```
02:00

↓

Collect Configurations

↓

Backup

↓

Compliance

↓

Generate Report

↓

Engineer Reviews Report
```

如果全部 PASS. 什么都不用做. 

如果出现 FAIL. 工程师根据 Report 分析原因. 

这里有一个重要的工程实践: 

>Compliance 的职责是发现问题(Detect)，而不是立即修复问题(Correct). 

是否需要自动修复(Remediation)，取决于企业的变更流程和风险控制. 

例如，在很多企业中，修复配置必须经过: 

Compliance Report ➡ Engineer Review ➡ Change Approval ➡ Maintenance Window ➡ Remediation

而不是 FAIL ➡ 立即修改设备

这种设计可以避免自动化误判导致的大规模配置变更. 

## 与后续章节的关系

截至本章结束，我们建立的是 Configuration Compliance Framework. 

它负责回答设备是否符合企业 Baseline? 

后续章节才会逐步扩展: 

- 如何管理越来越多的 Compliance Rules. 

- 如何生成更丰富的审计报告. 

- 如何在经过审批后执行自动化整改(Remediation). 

因此，本章到此为止，始终坚持 Detect First 的原则，不提前引入后续 Roadmap 的内容. 

## Chapter 9 第一阶段总结

经过本章前七节，我们已经构建了一个完整的企业级 Compliance Framework: 

```
Inventory
        │
        ▼
SSH Connection
        │
        ▼
Collect Running Configuration
        │
        ▼
Backup Configuration
        │
        ▼
Parse Configuration
        │
        ▼
Evaluate Compliance Rules
        │
        ▼
Generate Compliance Report
```

这一流程与 Chapter 8 的 Deployment Framework 相对应: 

| Deployment Framework   | Compliance Framework  |
| ---------------------- | --------------------- |
| Generate Configuration | Collect Configuration |
| Deploy Configuration   | Parse Configuration   |
| Push to Device         | Evaluate Rules        |
| Verify Deployment      | Generate Audit Report |

至此，你已经完成了企业自动化平台中的另一条核心工作流: Configuration Compliance & Audit. 