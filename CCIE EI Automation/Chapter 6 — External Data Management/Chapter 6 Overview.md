Chapter 6 Learning Objectives

# 完成本章后，读者将能够：

- 理解为什么企业将自动化数据与 Python 代码分离。
- 理解结构化数据（Structured Data）的基本概念。
- 编写和阅读基本的 YAML 文档。
- 使用 YAML 保存设备 Inventory。
- 理解 JSON 的基本结构与语法。
- 使用 Python 读取 JSON 数据文件。
- 比较 YAML 与 JSON 在网络自动化中的适用场景。
- 将现有 Inventory 从 Python 文件重构为外部数据文件，同时保持自动化程序逻辑不变。

虽然 Chapter 标题是 External Data Management，但实际上本章新增了唯一一个第三方 Python 库：

`pip install pyyaml`

实验环境中增加 

>Additional Python Package: PyYAML

# Chapter 6 Roadmap

6.1 Why External Data

为什么企业不会把设备信息写死在 Python 中。

6.2 YAML Fundamentals

学习 YAML 基本语法。

6.3 Building a YAML Device Inventory

使用 YAML 构建设备 Inventory。

6.4 JSON Fundamentals

学习 JSON 数据格式。

6.5 Reading JSON with Python

使用 Python 读取 JSON Inventory。

6.6 YAML vs JSON

比较两种数据格式在自动化中的特点与适用场景。

6.7 Inventory Refactoring

将前几章的 Python Inventory 平滑迁移到外部 YAML/JSON 文件，实现数据与代码分离，为后续章节（模板与接口）奠定基础。