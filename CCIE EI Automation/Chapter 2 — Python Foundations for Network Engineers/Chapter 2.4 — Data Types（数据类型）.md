
# Learning Objectives

完成本节后，你应该能够：

- 理解 Python 是强类型（Strongly Typed）语言

- 理解对象（Object）和类型（Type）的关系

- 掌握 Python 常用内置数据类型

- 使用 `type()` 查看对象类型

- 理解为什么类型决定对象能执行哪些操作

```
>>> hostname = "R1"
>>> print(type(hostname))
<class 'str'>
```

`<class 'str'>` 是什么意思?

表示 R1 的类型, 但是**变量没有类型，对象才有类型。**

这是 Python 一个非常重要的概念。

eg: `x = 10`

x 只是一个名字, 真正的数据是 10, 属于 int.


## 为什么 Python 需要数据类型？

不同的数据类型拥有不同的行为（Behavior）

int: 数学运算

str: upper(), lower(), replace(), split()

## Python 是 Strongly Typed

与一些弱类型语言不同，Python 不会随意把字符串当成数字处理。

| 类型      | 名称                  | 示例                     |
| ------- | ------------------- | ---------------------- |
| `str`   | String（字符串）         | `"R1"`                 |
| `int`   | Integer（整数）         | `100`                  |
| `float` | Floating Point（浮点数） | `3.14`                 |
| `bool`  | Boolean（布尔值）        | `True`、`False`         |
| `list`  | 列表                  | `["R1", "R2"]`         |
| `tuple` | 元组                  | `("R1", "R2")`         |
| `dict`  | 字典                  | `{"host": "10.1.1.1"}` |
| `set`   | 集合                  | `{"R1", "R2"}`         |

### 变量有类型

