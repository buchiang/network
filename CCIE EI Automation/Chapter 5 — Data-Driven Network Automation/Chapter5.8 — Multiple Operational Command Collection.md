Learning Objectives

完成本节后，你将能够：

- 理解为什么企业自动化通常一次执行多个 Operational Commands

- 在一次 SSH Session 中执行多个 Show Commands

- 使用 Python List 管理多个 Show Commands

- 理解"设备 Inventory"与"命令 Inventory"是两个不同的数据集合

- 为后续 Operational Data Collection 建立统一的数据组织方式

现在我们已经能批量执行 `show version` 

inventory ➡ connect ➡ show version  ➡  disconnect

生产环境中, 工程师很少只执行一个 show command, 在排查一台路由器时, 通常需要:

```
show version
show ip interface brief
show ip route
show clock
```

这里引出 operational commands 用于观察设备运行状态, 而不会修改设备配置的命令

- 不修改 Running Configuration

- 不影响业务

- 用于观察网络状态

在 [main 5.7.py](<LAB/main 5.7.py>) 已经有了一个 command list, 现在添加新的命令只需要`command.append("show inventory"), 这里只是补充一下 Python 语法, 正常人会选择改文件

[main 5.8 .py](<LAB/main 5.8.py>)

本章知识点较少, 因为之前在 5.7 中已经讲过 command list 这里不过是多加了一个 for 循环

