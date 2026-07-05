# Learning Objectives

完成本节后，你应该能够回答下面这些问题，而不仅仅是会写代码。

- SSH 为什么能够安全地远程管理 Cisco 设备？

- Netmiko 登录设备时，底层到底发生了什么？

- 一个 SSH Session 包含哪些组成部分？

- Cisco IOS 如何处理 SSH 连接？

- 企业为什么几乎全部采用 SSH，而不再使用 Telnet？

- 自动化脚本为什么必须理解 SSH，而不能只会调用 `ConnectHandler()`？

在 Linux SSH 到设备时, 由于有些老设备支持的 SSH 协议较老, 特别是 Ubuntu 已经仅用了这些老协议, 就会出现

```
user@ubuntu22-desktop:~$ ssh admin@12.1.1.1 Unable to negotiate with 12.1.1.1 port 22: 
no matching key exchange method found. 
Their offer: 
diffie-hellman-group-exchange-sha1,
diffie-hellman-group14-sha1
```
在设备上 `show ip ssh` 查看支持什么协议, 当然报错也告诉你支持哪些协议了

在 Linux 上

```
ssh \
-oKexAlgorithms=+diffie-hellman-group14-sha1 \
-oHostKeyAlgorithms=+ssh-rsa \
-oPubkeyAcceptedAlgorithms=+ssh-rsa \
admin@12.1.1.1
```

#### Netmiko：

负责 Cisco 自动化。

例如：

- 登录

- Prompt 判断

- 自动等待

- Enable Mode

- CLI Buffer

#### Paramiko：

负责 SSH 协议。

例如：

- Key Exchange

- Encryption

- Authentication

- SSH Channel

#### Cisco IOS：

负责解释 CLI。

例如：

show ip interface brief

IOS 返回：

Interface

IP Address

Status

Protocol
...

## SSH 到底是什么？

很多教材说 SSH 是 Secure Shell。这句话没有错，但工程上意义不大。

更准确的理解是 SSH 是一个在不可信网络上建立安全远程终端会话（Secure Remote Terminal Session）的协议。

SSH 完成四件事情：

1. 身份认证(Authentication) 确认你是谁？

2. 加密(Encryption) 保证别人看不到通信内容。

3. 完整性(Integrity) 保证数据没有被修改。

4. 会话(Session) 建立一个远程 CLI。

**所以 SSH ≠ 登录 SSH = 安全终端**

## SSH Session 的组成

建立 SSH 后，会形成一个 Session。

Ubuntu

│

SSH Session

│

Cisco IOS

│

CLI

这个 Session 里面包含：

Authentication

↓

Encryption

↓

Channel

↓

CLI

↓

Prompt

其中最重要的是 **SSH Channel** SSH 并不是每执行一次命令就建立一次 TCP。

而是：

SSH Connection

↓

SSH Channel

↓

show version

↓

show ip int brief

↓

show run

↓

copy run start

↓

exit

全部共用一个 Channel。

所以 Netmiko 的一个连接对象 `net_connect` 实际上对应一个 SSH Session + 一个 SSH Channel

这也是为什么 `net_connect.send_command()` 可以连续执行几百条命令。

## Cisco IOS 如何处理 SSH？

很多人认为 SSH 登录以后：

Python

↓

Cisco

实际上，中间还有：

Python

↓

SSH

↓

VTY

↓

EXEC

↓

CLI

Cisco IOS 收到 SSH 后首先进入 VTY Line。

例如 line vty 0 4 然后创建一个 EXEC Session。

例如 `R1>` 随后进入 CLI。

因此Netmiko 实际是在控制一个远程终端，而不是调用 Cisco API。

## Cisco CLI Prompt

Prompt 非常重要。

`R1>` 表示 User EXEC。

`R1#` 表示 Privileged EXEC。

`R1(config)#` 表示 Global Config。

Netmiko 会不断检测 Prompt。

例如：

R1#

↓

发送命令

↓

等待 Prompt 返回

↓

继续下一条命令

所以 Prompt 是 Netmiko 判断 命令是否执行完成的重要依据。

## 为什么 Netmiko 比 Paramiko 更适合 Cisco？

如果使用 Paramiko 你需要自己处理：

recv()

buffer

sleep()

prompt

timing

pagination

全部自己写。

Netmiko 已经全部做好。

例如：

```
output = net_connect.send_command(
    "show version"
)
```

Netmiko 内部实际上做了：

发送命令

↓

等待 Prompt

↓

读取 Buffer

↓

去掉 Echo

↓

处理分页

↓

返回字符串

因此：

企业几乎都是：

Netmiko

Scrapli

NAPALM

而不是直接 Paramiko。

## Cisco Implementation

下面确认你的 IOSv 已经具备 SSH 条件。

### 查看 VTY 配置

`show running-config | section line vty`

应类似：

```
line vty 0 4
 login local
 transport input ssh
```

### 查看 SSH 状态

`show ip ssh`

如果启用成功，应看到类似信息：

```
SSH Enabled
Authentication timeout
Version 2.0
```

### 查看当前 SSH 会话

`show users`

登录后会显示：

```
R1#show users
    Line       User       Host(s)              Idle       Location
*  0 con 0                idle                 00:00:00
   2 vty 0     admin      idle                 00:00:02 10.10.10.100

  Interface    User               Mode         Idle     Peer Address
```
这说明 SSH Session 已建立。

可以看到 SSH 占用的是 VTY(Virtual Teletype) 线路, 而不是物理 Console 口。每建立一个 SSH 会话，IOS 就会分配一个空闲的 VTY Line，并为其创建对应的 EXEC Session。

### Configure

如果 SSH 尚未启用，可按以下步骤配置：

```
conf t

hostname R1
ip domain-name lab.local

username admin privilege 15 secret cisco123

crypto key generate rsa modulus 2048

ip ssh version 2

line vty 0 4
 login local
 transport input ssh

end
write memory
```

## Troubleshooting

| 现象                    | 可能原因              | 验证命令                                      | 解决方法                                     |
| --------------------- | ----------------- | ----------------------------------------- | ---------------------------------------- |
| Connection refused    | SSH 服务未启用         | `show ip ssh`                             | 配置 RSA Key、启用 SSH                        |
| Authentication failed | 用户名或密码错误          | `show running-config \| section username` | 检查本地用户配置                                 |
| Timeout               | IP 不可达或 ACL 阻断    | `ping`、`show ip interface brief`          | 检查连通性与接口状态                               |
| 登录后立即断开               | VTY 配置错误          | `show running-config \| section line vty` | 配置 `login local` 与 `transport input ssh` |
| 卡在命令输出                | 分页未关闭（某些 SSH 客户端） | `show terminal`                           | Netmiko 通常会自动处理分页                        |


## Engineering Notes（企业最佳实践）

1. 统一启用 SSH Version 2，避免使用已淘汰的 SSHv1。

2. RSA 密钥长度建议至少 2048 位，满足现代安全要求。

3. 仅允许 SSH 登录 VTY：

`transport input ssh`

不要同时开放 Telnet，除非有特殊兼容需求。

1. 为自动化账号使用最小权限原则。实验环境可使用 privilege 15，生产环境应结合 AAA、TACACS+ 或 RADIUS 实现精细授权。

2. 自动化脚本应优先检测 SSH 是否可达，而不是直接执行配置操作。

## Chapter Summary

本节建立了 Netmiko 自动化所依赖的 SSH 基础模型，重点包括：

- 理解 Python → Netmiko → Paramiko → SSH → Cisco IOS 的完整调用链。

- 理解 SSH Session、SSH Channel、VTY 与 Cisco CLI 的关系。

- 掌握 Cisco IOS 为 SSH 提供服务所需的基本配置。

- 学会通过 show ip ssh、show users 等命令验证 SSH 服务状态。

- 建立了后续编写自动化脚本所需的底层认知。