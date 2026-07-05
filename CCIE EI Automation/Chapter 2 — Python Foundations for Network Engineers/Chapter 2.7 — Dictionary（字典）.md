
# Learning Objectives

完成本节后，你应该能够：

- 理解 Dictionary 的本质

- 理解 Key-Value（键值对）

- 理解为什么 Dictionary 比 List 更适合描述网络设备

- 掌握增删改查

- 理解 Dictionary 与 JSON 的关系

- 为后续 Netmiko、RESTCONF、PyATS 做准备

## 什么是 Dictionary？

Key → Value 的映射（Mapping）

```
device = {
    "hostname": "R1",
    "host": "10.1.1.1"
}
```

## Value 可以是什么？

几乎任何对象。

例如：

```
device = {
    "hostname": "R1",
    "port": 22,
    "enabled": True
}
```

Value 可以是：String, Integer, Boolean, List, Dictionary, Tuple …

## Nested Dictionary（嵌套字典）

```
device = {
    "hostname": "R1",
    "management": {
        "ip": "10.1.1.1",
        "mask": "255.255.255.0"
    }
}
```

## 常用操作

读取：

`print(device["hostname"])`

修改：

`device["hostname"] = "EDGE-01"`

增加：

`device["location"] = "Frankfurt"`

删除：

`del device["password"]`

判断：

`"host" in device`

## Cisco Automation Example

真正的 Netmiko：

```
device = {
    "device_type": "cisco_ios",
    "host": "10.1.1.1",
    "username": "admin",
    "password": "Cisco123"
}
```

以后：

`conn = ConnectHandler(**device)`

## 更进一步（真正企业项目）

企业里面通常不是一个设备。而是很多设备。

于是就变成：

```
devices = [
    {
        "hostname": "R1",
        "host": "10.1.1.1",
        "username": "admin",
        "password": "Cisco123"
    },
    {
        "hostname": "R2",
        "host": "10.1.1.2",
        "username": "admin",
        "password": "Cisco123"
    }
]
```

这里其实是：

```
List
 │
 ├── Dictionary
 ├── Dictionary
 └── Dictionary
```

这就是 CCIE 自动化最经典的数据结构。以后几乎所有项目都会长这样。