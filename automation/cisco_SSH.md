! 1. 域名 —— 生成密钥的前提

ip domain name lab.local

! 2. 生成 RSA 密钥，SSHv2 要求至少 2048 位

crypto key generate rsa modulus 2048

! 3. 本地账号（netmiko 登录用）

username admin privilege 15 secret cisco123

! 4. enable 密码（netmiko 进特权模式用）

enable secret cisco123

! 5. 强制 SSHv2

ip ssh version 2

! 6. VTY 只允许 SSH，用本地账号认证

line vty 0 4
 transport input ssh
 login local
exit

end
write memory