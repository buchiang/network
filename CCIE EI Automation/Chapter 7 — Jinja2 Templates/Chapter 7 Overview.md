Chapter 7 将继续保持统一工程目录。

```
Lab/

├── automation/
│
├── inventory/
│
├── templates/
│
├── configs/
│
├── modules/
│
├── output/
│
└── logs/
```

新增目录：`templates/`

后续所有模板全部放入：`templates/`

生成后的配置统一放入：`output/`

保持 Data 与 Template 完全分离。

# Learning Objectives

完成本章后，读者应能够：

- 理解为什么企业网络需要模板（Templates）

- 理解 Template Engine 的工作方式

- 编写基础 Jinja2 Template

- 使用变量生成配置

- 使用表达式（Expressions）

- 使用循环（Loops）

- 使用条件（Conditions）

- Render Template

- 将数据与模板彻底解耦

- 完成企业级 Template Refactoring