# Networking Lab – Cisco Routing & Switching Practice

所有都基于我在EVE-NG上的实验笔记, 截止于12月已经包含 VLAN, STP, DHCP, OSPF, BGP, MPLS(未整理完毕), 后续计划整理 EIGRP, SDWAN. 以及可以考虑加入 English Version.

This repository contains my personal networking labs and study notes built using EVE-NG and Cisco IOS.
The purpose of this project is to strengthen my skills in routing, switching, troubleshooting, and network design while preparing for advanced networking roles and certifications.


## Topics Covered

This repository includes configuration examples, lab topologies, and notes for the following networking concepts:

### Layer 2

[VLAN & Trunk](VLAN)


[STP](STP.md)

Port Security (I forget sort it)

### Layer 3

[OSPF](OSPF)

EIGRP (Not yet)

[BGP](BGP)
 
[VRRP](DHCP/031025_VRRP.md) / [HSRP](DHCP/280925_HSRP.md)

Network Services

[DHCP](DHCP)

[NAT / PAT](Security/FIREWALL/DAY_25_NAT.md)

### Tunneling & VPN

[GRE](VPN/GRE.md)

[IPsec](VPN/DAY_41_BASIC_1.md)

### Security

[ACL](Security/ACL)

[Firewall](Security/FIREWALL)

## Home Lab Environment

All labs in this repository were built and tested in my personal home lab using:

EVE-NG Community Edition

Cisco IOS images 

Virtual PCs (VPCS), in Firewall I set the Linux PC, it has more function. 

Wireshark for packet capture and protocol analysis

This environment allows me to simulate enterprise network topologies and practice troubleshooting in a realistic setup.

## Planned Improvements

- This repository is continuously updated. Upcoming additions include:

    1. MPLS L3VPN fundamentals

    2. IPSec VPN configuration labs

    3. **Network automation basics (Python + Netmiko/NAPALM)**

    4. Advanced troubleshooting case studies

    5. SDWAN

    6. maybe a English Version

