telnetlib 是 python 内置模块, python 2 对应的是 telnetlib 2, python 3 对应 telnetlib 3.

```python
import telnetlib
import time

"""
define device information
"""
device_ip = "12.1.1.1"
username = "admin"
password = "cisco123"
enable_password = "cisco123"

"""
Creat Telnet conncetion
"""

tn = telnetlib.Telnet(device_ip)
time.sleep(1)

tn.read_until(b"Username: ") #waiting for the Username cli
tn.write(username.encode("utf-8") + b"\n")
time.sleep(1)
tn.write(password.encode("utf-8") + b"\n")
time.sleep(1)

tn.write(b"enable\n")
tn.write(enable_password.encode("utf-8") + b"\n")
time.sleep(1)
tn.write(b"show ip int brief\n")
time.sleep(1)

output = tn.read_all()
print(ouput.decode("utf-8"))

tn.close()
```

b "..." 代表字节串 适用telnet 通信

cli.recv() 接收