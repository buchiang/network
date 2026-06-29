# Netmiko 基础:连接、读取、配置下发

> Month-2 Automation / Lab 01
> 平台:EVE-NG,IOSv 15.7 + Ubuntu 22.04(Netmiko 4.7.0)
> 目标:从 Linux 用 Netmiko(Python)读取并配置 R1

## 拓扑

```
VSCode ──SSH──> Linux (ubuntu22-desktop)
                 ├─ ens3: 10.10.10.100/24  ──┐
                 └─ ens4: 192.168.178.144/24  │  10.10.10.0/24(自动化管理通道)
                                              │
                              R1 (IOSv 15.7) ─┘
                 ├─ e0/1: 10.10.10.1/24
                 └─ e0/0: dhcp → 192.168.178.143  →  Net(公网)
```

- VSCode 通过 SSH 连到 EVE-NG 里的 Linux 节点
- Linux `ens3` 与 R1 `e0/1` 同处 `10.10.10.0/24`,这是脚本控制 R1 的管理通道
- R1 `e0/0` 走 DHCP 接入家庭网/公网(`192.168.178.0/24`)

---

## 一、R1 侧:开启 SSH(前提)

Netmiko 的 `cisco_ios` 默认走 SSH(TCP 22),所以 R1 必须先具备 SSH server:

```
conf t
 hostname R1
 ip domain name lab.local
 crypto key generate rsa modulus 2048
 ip ssh version 2
 username admin privilege 15 secret cisco123
 line vty 0 4
  login local
  transport input ssh
end
write memory
```

要点:
- `crypto key generate rsa` 必须在 `hostname` + `ip domain name` 之后,否则报 `% Please define a domain-name first`
- modulus ≥ 768 才能跑 SSHv2,直接给 2048
- `ip domain name`(带空格)是 15.x 写法;老镜像若报错改用 `ip domain-name`(连字符)
- admin 给 `privilege 15`:连上即特权模式,脚本无需再过 enable

---

## 二、Linux 侧:环境确认

```bash
pip show netmiko              # 确认已安装(本 lab 用 4.7.0,ntc-templates 随依赖一起装好)
ping 10.10.10.1               # 验证到 R1 可达
```

---

## 三、第一个脚本:读

`r1.py`:

```python
from netmiko import ConnectHandler

r1 = {
    "device_type": "cisco_ios",
    "host": "10.10.10.1",
    "username": "admin",
    "password": "cisco123",
    "secret": "cisco123",       # priv 15 用不到;降权时作 enable 兜底
}

with ConnectHandler(**r1) as conn:   # with 出块自动 disconnect,抛异常也照关
    conn.enable()                    # priv 15 已在特权模式,这步自动跳过,留作防御
    print(conn.find_prompt())
    print(conn.send_command("show ip interface brief"))
```

正常输出:

```
R1#
Interface                  IP-Address      OK? Method Status                Protocol
Ethernet0/0                192.168.178.143 YES DHCP   up                    up
Ethernet0/1                10.10.10.1      YES manual up                    up
Ethernet0/2                unassigned      YES unset  administratively down down
Ethernet0/3                unassigned      YES unset  administratively down down
```

---

## 四、结构化数据:从文本到 list[dict]

同一条命令加 `use_textfsm=True`(依赖 ntc-templates),返回可编程的数据结构:

```python
data = conn.send_command("show ip interface brief", use_textfsm=True)
for row in data:
    print(row["interface"], row["ip_address"], row["status"])
# 每个 row 是 dict:{'interface': 'Ethernet0/0', 'ip_address': '192.168.178.143', 'status': 'up', ...}
```

这是自动化真正的分水岭——从"打印一坨文本"到"按字段取值、做判断/比对"。

---

## 五、配置下发 + 保存

```python
cfg = [
    "interface Loopback0",
    "ip address 1.1.1.1 255.255.255.255",
    "description set-by-netmiko",
]
with ConnectHandler(**r1) as conn:
    conn.enable()
    print(conn.send_config_set(cfg))     # 自动进 conf t、逐行下发、退出
    print(conn.save_config())            # 等价 write memory
    print(conn.send_command("show ip int brief | include Loopback0"))
```

---

## 六、验证命令(R1 侧)

```
show ip ssh             # SSH Enabled - version 2.0 → key 已生成、SSHv2 就绪
show ssh                # 当前活动的 SSH 会话(能看到脚本连进来的那条)
show users              # 当前登录的线路与来源 IP
```

---

## 七、常见坑(实战记录)

### 1. 主机侧 IP 重复(本次卡最久的根因)

**现象**:`ping 10.10.10.1` 通,但 `ssh admin@10.10.10.1` 弹出密码框后 `Permission denied`。
**根因**:desktop 自己的 `ens3` 也配了 `10.10.10.1`,与 R1 `e0/1` 撞车。Linux 见目标是本机地址,直接走 loopback——包没出网卡,全程在跟自己说话(本机无 `admin` 用户故拒绝),R1 全程没被碰到。

判断"回应你的是 IOS 还是 Linux":

| 信号 | IOSv | Linux / OpenSSH |
|------|------|-----------------|
| ping 的 TTL | 255 | 64 |
| SSH host key 类型 | RSA | ED25519(默认) |
| 直连延迟 | 0.x–几 ms | ~0.02 ms(本机栈) |
| 失败措辞 | IOS 自有提示 | `Permission denied (publickey,password)` |

**定位**:`ip -br addr` 看本机所有 IP;若 `.1` 落在本机,改回 `.100`:

```yaml
# /etc/netplan/xx.yaml — 网卡名换成朝 R1 那一侧
    ens3:
      addresses: [10.10.10.100/24]
```
```bash
sudo netplan apply
# NetworkManager 托管:nmcli con mod <名> ipv4.addresses 10.10.10.100/24 && nmcli con up <名>
```

> 教训:开工不仅要核 R1 的 `show ip int br`,也要核**主机自己**的 `ip -br addr`。地址串位这次串在主机侧。

### 2. SSH KEX / host key 算法不匹配

**现象**:改对 IP 后,手工 `ssh` 报 `no matching key exchange method found`,连密码框都不弹。
**根因**:OpenSSH 8.8+ 默认禁用 SHA-1 系 KEX 与 `ssh-rsa`(SHA-1 签名,已被碰撞攻破);IOSv 15.7 只会 `diffie-hellman-group14-sha1` / `group-exchange-sha1`,两边交集为空,在认证前就谈崩。
**关键区别**:这堵墙挡 OpenSSH 命令行,**但不挡 Netmiko**——Netmiko 走 Paramiko,Paramiko 算法表里仍保留 `group14-sha1`,能与 R1 谈拢。所以脚本可直接跑通,无需改任何 ssh 配置(`~/.ssh/config` 不作用于 Paramiko)。

要让**手工 ssh** 也能进(排错方便):

```
# ~/.ssh/config
Host 10.10.10.*
    KexAlgorithms +diffie-hellman-group14-sha1
    HostKeyAlgorithms +ssh-rsa
```
- `+` 是在默认集合上"加回",不影响连其他现代主机
- `HostKeyAlgorithms +ssh-rsa` 必须一并加,否则过了 KEX 会立刻撞到 host key 那道一样的墙
- `Host 10.10.10.*` 只覆盖 lab 段,不碰 `ens4` 的管理网

### 3. known_hosts 残留

修 IP 期间若先把"假 `.1`"(Linux 的 ED25519)存进了 `known_hosts`,等 `.1` 变回 R1(RSA key)再 ssh 会报 `REMOTE HOST IDENTIFICATION HAS CHANGED`:

```bash
ssh-keygen -R 10.10.10.1
```

### 4. priv 15 vs enable

admin 是 `privilege 15` → 连上即特权模式,`conn.enable()` 自动跳过。一旦把用户降到 `privilege < 15`,字典里必须有 `secret`,`.enable()` 才能登上去。

---

## 八、下一步(Month-2 路线)

- [x] 01 Netmiko:连接 / 读 / 结构化数据 / 配置下发 ← 本篇
- [ ] 02 多设备 + inventory(循环、YAML 设备表、并发)
- [ ] 03 NAPALM:getters、config replace / merge、rollback
- [ ] 04 NETCONF / RESTCONF(需 IOS-XE,搬到 CML;`netconf-yang` / `restconf` + ncclient / requests)
- [ ] 05 EEM applet(syslog / track 触发)
- [ ] 06 DNAC / Catalyst Center API(DevNet Sandbox)
