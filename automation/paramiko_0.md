
1. netmiko 是基于 Paramiko 开发的, 因此在安装 Netmiko 时, Paramiko 会作为依赖项自动安装

2. 如果只需要 paramiko, 可以单独安装 Paramiko

目标 通过 Paramiko 实现与网络设备的 SSH 连接, 学习如何发送命令并动态配置设备.

1. 使用 SSH 连接网络设备

2. 进入 enable 模式, 完成基本的设备配置

3. 使用 Paramiko 的 invoke_shell 实现交互式 CLI 操作

4. 理解延迟的必要性, 确保设备命令正常执行

5. 解决分页问题和长数据读取的问题

## 如何进行 SSH 连接

1. 打开 ssh 客户端

2. 连接 ssh 服务端 输入 ip, 用户名和密码

3. 保存 rsa 的非对称公钥用于后续的数据加密

4. 连接到设备后输入 enable 密码登陆到设备

5. 输入 conf t 进入配置模式

6. 输入所需要的命令

7. 关闭 ssh 客户端, 断开 ssh 连接释放资源

# 通过 paramiko 给设备接口配置 IP

```
import paramiko
import time #导入 python 自带时间模块, 用于添加必要延迟, 防止卡顿

device_ip = "10.10.10.1"
username = "admin"
password = "cisco123"
enable = "cisco123"

#创建 SSH 客户端
ssh_client = paramiko.SSHClient()
ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy()) #自动接受未知主机密钥

#连接设备
try:
    print("连接到设备...")
    ssh_client.connect(hostname=device_ip, username=username, password=password)
except:
    print("连接失败")
else:
    print("成功连接到设备")

#开启交互式 CLI 通道
try:
    cli = ssh_client.invoke_shell() #的打开 CLI 通道
except:
    print("开启 CLI 失败")
else:
    print("CLI 通道已建立")

#进入 Enable
cli.send("enable\n")
time.sleep(1) #添加等待时间
cli.send(enable + "\n") #输入 enable 密码
time.sleep(1)

#检查是否成功进入 Enable
oupt = cli.recv(5000).decode("utf-8") #recv-receive 5000 表示接受5000字节的数据
print(output)
if "#" in output:
    print("成功进入 Enable 模式")
else:
    print("进入 Enable 模式失败")
    ssh_client.close()
    exit()
```