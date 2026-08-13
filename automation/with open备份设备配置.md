with open 的好处

自动管理文件的打开和关闭
语法简单, 易于维护
会自动打开与关闭文件

```python
with open("example.txt" "w") as file:
    file.write("xxx")

with open("example.txt" "r") as file:
    content = fi;e.read()
    print(content)

```

read() 全部读取

readline() 一行一行读取

readlines() 返回的值是列表

## open() 函数

```python
file = open("example/x/x.txt", "r", encoding = "utf8")#如果有中文 需要 utf8 编码
content = file.read()
print(content)
```

r+, w+ 都可以理解为既打开也写入
a+ 也是既打开也追加

file.seek()

移动文件指针到开头, 因为 python 读取是从光标位置后面的内容

```python
file = open("xxx", "a+", encoding = "utf8")
file.write("xxx")
file.seek()
file.close()
content = file.read()
print(content)
```

with open 就不需要 file.close()

