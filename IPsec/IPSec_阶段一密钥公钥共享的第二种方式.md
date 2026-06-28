
之前一直使用的方式是

`Router(config)#crypto isakmp key acc address 0.0.0.0`

这种方式的特点:

1. 不支持 VRF

2. 空格不算密码

第二种

```
Router(config)#crypto keyring PASSWORD0 ?
  vrf  Mention a vrf it belongs to
  <cr>
```

后面可以挂 VRF, 如果直接回车就是全局模式

```
Router(config)#crypto keyring PASSWORD0
Router(conf-keyring)#pre-shared-key address 0.0.0.0 key abc   
% Warning: Trailing white space(s) detected for the preshared key
```

虽然文本里看不到我敲了空格, 但是我确实敲了空格, 系统也提示了空格也算密码

如果是基于 VRF 的 IPSec 配置, 就必须使用第二种密钥共享方式

*PS: 两种模式可以共存, 当然前提是密码必须一致*