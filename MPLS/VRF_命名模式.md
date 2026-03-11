
除了普通模式设置 VRF 外, 还可以使用命名模式来设置 VRF.

```
PE_2(config)#vrf definition SPOKE2
PE_2(config-vrf)#rd 10000:10

PE_2(config-vrf)#address-family ?
  ipv4  Address Family
  ipv6  Address Family

PE_2(config-vrf)#address-family ipv4
PE_2(config-vrf-af)#route-target 100:10

PE_2(config-vrf)#address-family ipv6
PE_2(config-vrf-af)#route-target 200:10
```

在命名模式种, 可以同时设置 ipv4 与 ipv6 他们使用相同的 RD , 但是可以分别设置所需要对应的 RT

```
PE_2#show vrf brief SPOKE2
  Name                             Default RD            Protocols   Interfaces
  SPOKE2                           10000:10              ipv4,ipv6
PE_2#
PE_2#show vrf de
PE_2#show vrf detail SPOKE2
VRF SPOKE2 (VRF Id = 2); default RD 10000:10; default VPNID <not set>
  New CLI format, supports multiple address-families
  Flags: 0x180C
  No interfaces
Address family ipv4 unicast (Table ID = 0x2):
  Flags: 0x0
  Export VPN route-target communities
    RT:100:10
  Import VPN route-target communities
    RT:100:10
  No import route-map
  No global export route-map
  No export route-map
  VRF label distribution protocol: not configured
  VRF label allocation mode: per-prefix
Address family ipv6 unicast (Table ID = 0x1E000001):
  Flags: 0x0
  Export VPN route-target communities
    RT:200:10
  Import VPN route-target communities
    RT:200:10
  No import route-map
  No global export route-map
```