# Learning Objectives

完成本节后，你将能够：

* 理解为什么企业自动化项目需要统一的目录结构。

* 学会按照职责组织项目文件。

* 区分代码、日志和运行结果的存放位置。

* 建立适合长期维护的基础项目结构。

* 为 Chapter 5 的数据驱动自动化做好工程准备。

经过前面的学习，我们已经把代码拆分成多个模块。

例如：

```text
automation/
│
├── automation.py
└── device.py
```

对于当前实验，这样已经足够, 但是假设项目继续发展, 新的需求不断增加：

* 保存运行日志

* 保存设备输出

* 新增多个 Python 模块

* 多个工程师共同开发

项目很快可能变成：

```text
automation/
│
├── automation.py
├── device.py
├── backup.txt
├── automation.log
├── result.txt
├── test.py
├── new.py
├── temp.py
└── old.py
```

所有文件都放在同一个目录, 虽然程序仍然能够运行, 但是维护成本开始迅速增加。


企业项目通常遵循一个基本原则：

> **Files Should Be Organized by Responsibility.**

也就是说：

> 文件按照职责分类，而不是按照创建时间分类。

例如：

Python 源代码-应该放在一起。

日志文件-应该放在一起。

程序运行产生的数据-也应该放在一起。

这样任何工程师进入项目, 都能够快速找到需要的内容。

## 为什么目录结构如此重要？

### 原因一：提高可维护性

假设某一天需要修改 SSH 登录函数。如果所有 Python 文件都混在一起, 需要逐个寻找。

如果所有源码都集中管理, 维护效率会明显提高。

### 原因二：方便定位问题

假设程序运行失败, 第一步应该查看日志。如果日志文件散落在不同目录, 排查问题会更加困难。

统一目录意味着统一定位方式。

### 原因三：方便团队协作

多个工程师共同开发时, 通常都会约定代码放哪里, 日志放哪里, 运行结果放哪里。

统一目录结构能够减少沟通成本。

## Cisco Implementation

假设企业每天凌晨执行： `Configuration Backup` 运行结束后通常会产生两类内容。

### 第一类：程序运行记录。

例如：`automation.log`


### 第二类：设备业务数据。

例如：`R1_show_version.txt`

这两类文件职责完全不同。因此不应该混合存放。

## Observe

当前项目：

```text
automation/
│
├── automation.py
├── device.py
└── automation.log
```

所有内容位于同一级目录。

## Verify

观察下面三个对象：

```text
device.py

automation.log

show version 输出
```

它们职责是否相同？

答案: 不是。

因此不应该长期放在同一个位置。

## Analyze

建立统一目录, 建议如下：

```text
automation/
│
├── automation.py
├── device.py
├── logs/
└── output/
```

职责：

automation.py ➡ Workflow ➡ device.py ➡ Device Capability ➡ logs/ ➡ 运行日志 ➡ output/ ➡ 设备输出

目录开始具有明确职责。

## Configure

创建目录：

```bash
mkdir logs
mkdir output
```

修改 Logging。

原来：

```python
logging.basicConfig(
    filename="automation.log",
)
```

修改为：

```python
logging.basicConfig(
    filename="logs/automation.log",
)
```

这样日志统一进入 logs/ 后续如果保存 show version 输出, 统一放入 output/

注意本章暂不实现保存设备输出, 这里只完成目录规划。

## Verify Again

运行程序确认日志已经生成：

```text
automation/
│
├── logs/
│   └── automation.log
```

说明目录调整成功, 程序行为保持一致。

---

# Troubleshooting

### 问题一：为什么提示：

```text
No such file or directory
```

通常说明 logs/ 目录尚未创建。

请确认：

```bash
mkdir logs
```

已经执行。

### 问题二：为什么日志没有进入：

logs/ 请检查：

```python
filename="logs/automation.log"
```

路径是否正确。另外确认 `logging.basicConfig()` 在程序开始阶段执行。

### 问题三：为什么现在就建立：

output/ 目前虽然还没有正式保存 CLI 输出, 但是提前建立目录。可以保持项目结构稳定, 后续新增功能无需再次调整目录。

## Engineering Notes

本节建立一个重要工程实践：

> **Separate Source Code from Runtime Data.**

也就是源码, 运行日志, 业务数据分别管理, 不要全部放在项目根目录。随着项目规模扩大这种目录组织方式能够显著提高可维护性。另外，本 Workbook 从本章开始统一采用以下基础目录规范：

```text
automation/
│
├── automation.py
├── device.py
├── logs/
└── output/
```

后续章节会在此基础上逐步扩展，而不会推翻已有结构。