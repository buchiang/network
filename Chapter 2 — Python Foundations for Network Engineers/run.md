

ip domain name lab.local

username admin privilege 15 secret cisco123

enable secret cisco123

crypto key generate rsa modulus 2048

ip ssh version 2

R1(config)#line vty 0 4
R1(config-line)#login local
R1(config-line)#transport input ssh

```
ip domain name lab.local
username admin privilege 15 secret cisco123
enable secret cisco123
crypto key generate rsa modulus 2048
ip ssh version 2
line vty 0 4
login local
transport input ssh
end
wr
```