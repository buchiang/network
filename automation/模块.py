"""

import requests

import netmiko

import parmiko
"""
"""
parmiko 低级 ssh 连接每一行命令需要手写
netmiko 高级 ssh 连接可以直接传入命令列表，自动执行
requests 发送 http 请求
"""

import os

dir = os.getcwd()
print("当前工作目录为：", dir)
items = os.listdir(dir)
print("当前目录下的文件和文件夹有：")
for item in items:
    print(item)