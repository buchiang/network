- BGP (Border Gateway Protocol) is an External Gateway Protocol (EGP). Network gateway protocols are classified into two categories:

    1. IGP (Internal Gateway Protocol): Used within an organization (e.g., OSPF, EIGRP).

    2. EGP (External Gateway Protocol): Used to connect different Autonomous Systems. BGP is the standard EGP for modern internet routing.

1. **Why BGP?**

- As network scales grow, IGPs (OSPF, EIGRP) cannot handle the massive volume of global routes. This led to the creation of the Autonomous System (AS).

        Definition: An AS is a collection of IP networks and routers under a single administrative domain that follows a unified routing policy.

    - Identification: Each AS is identified by an AS Number (ASN) (16-bit or 32-bit), distributed by IANA.

    - Role of BGP: BGP facilitates communication between different AS domains.

- **BGP vs. Traditional IGP**

The "Courier" Concept: BGP acts as a routing information courier. It doesn't "calculate" the best path using physics-based metrics (like bandwidth); it "picks" the path based on administrative Policies.

2. BGP Evolution
1980s: EGP appeared, followed by BGP-1 in 1989.

BGP-4+ (Multiprotocol BGP / MP-BGP): The current standard. Unlike BGP-4 (IPv4 only), MP-BGP supports multiple address families: IPv6, VPNv4, VPNv6, and L2VPN.

Core Characteristics
TCP 179: Sessions are established over stable TCP connections.

Scalability: Capable of carrying massive routing tables (the global Internet table now exceeds 1 million prefixes).

Policy Flexibility: Uses attributes like AS-PATH, Local Preference, MED, and Community for granular traffic engineering.

MPLS/VPN Integration: Essential for passing customer VPN labels in service provider networks.

Stability: Features like Route Aggregation and Route Dampening prevent network-wide instability from local route flapping.

3. BGP Security & Authentication
Common Attack Vectors
Unauthorized Peering: Establishing illegal neighbor relationships to inject malicious routes.

Resource Exhaustion: Flooding BGP control packets to spike CPU utilization.

Security Mechanisms
MD5 Authentication: Configured during the TCP handshake. The password is part of the TCP segment, ensuring that only authorized peers can establish a session.

Keychain Authentication: Allows for dynamic password rotation without manual intervention (Common in Huawei/Cisco).

GTSM (Generalized TTL Security Mechanism):

Filters packets based on the TTL (Time-to-Live) value.

Logic: For direct EBGP peers, the TTL is expected to be 255. If an attacker tries to spoof a packet from outside the local subnet, the TTL will drop below 255 after passing through a router, and GTSM will discard it.

4. Laboratory Configuration: Multi-hop Peering
BGP allows establishing neighbor relationships across multiple hops, provided there is IP reachability (usually via Static routes or IGP).

Scenario: Peering via Loopback Interfaces
1. Establish IP Reachability (Static Routes):

2. Configure BGP (EBGP Multi-hop):

3. Verification:

5. Route Advertisement & Inter-AS Communication
When a prefix is advertised via the network command, it must exist in the local routing table (RIB).

The Reachability Challenge
Even if BGP distributes the route 1.1.1.1/32 to AS 20000, internal routers in AS 20000 (like R4) may not know how to reach it.

The Problem: BGP routes are typically NOT redistributed into local IGPs (OSPF/EIGRP) due to the massive size of the BGP table.

The Solution: Use Default Routes or specific Static Routes pointing toward the BGP exit routers (R2/R3) for internal connectivity.