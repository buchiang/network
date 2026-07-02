
# Learning Objectives

完成本节后，你应该能够：

- 理解什么是 List

- 理解 List 为什么是有序（Ordered）的

- 理解索引（Index）

- 掌握增删改查

- 理解 Mutable（可变对象）

- 能够遍历 List

- 在 Cisco Automation 中使用 List

## Index（索引）

```
devices = ["R1", "R2", "R3"]
print(devices[0])
```

结果

R1

### Negative Index

Python 很方便。

最后一个：

`devices[-1]`

得到：

R3

倒数第二：

`devices[-2]`

得到：

R2

## Mutable（可变对象）

`devices[0] = "EDGE-01"`

现在：

`print(devices)`

输出：

`['EDGE-01', 'R2']`

