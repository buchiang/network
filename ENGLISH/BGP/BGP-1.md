

- BGP (Border Gateway Protocol) is an External Gateway Protocol (EGP). Network gateway protocols are generally classified into two categories:

    -  IGP (Internal Gateway Protocol): Used within an Autonomous System (e.g., OSPF, EIGRP, IS-IS).

    - EGP (External Gateway Protocol): Used to exchange routing information between 
different Autonomous Systems. BGP is the industry-standard EGP today.

**Why BGP?**

While IGPs like OSPF and EIGRP are efficient within an organization, they 
cannot scale to manage the massive routing tables of the global Internet. This 
limitation led to the development of the Autonomous System (AS).

    Definition: An AS is a collection of IP networks and routers under the control of a single technical administration that presents a common routing policy to the Internet.

Different AS domains are distinguished by unique AS Numbers (ASN). ASNs are 
available in 16-bit and 32-bit formats, with distribution managed by *IANA*.

**BGP vs. Traditional IGP**

BGP functions more like an Application Layer protocol rather than a traditional 
routing protocol.

1. Transport & Reliability (TCP 179)
    - Mechanism: BGP uses TCP port 179 for transport. As long as TCP connectivity is established, BGP can form a stable neighbor relationship.

    - Contrast: Traditional IGPs (OSPF, EIGRP) use raw IP packets and must handle their own reliability (e.g., OSPF's LS Acknowledgment). BGP offloads reliability to the TCP layer, eliminating the need for custom acknowledgment mechanisms.

2. The "Courier" Concept

    - Role: BGP does not "calculate" routes; it carries them. It acts as a courier for routing information.

    - Behavior: IGPs use algorithms (like SPF/Dijkstra) to discover the network and  calculate the best path. BGP relies on manual configuration (via the network command) or redistribution from an IGP to originate and propagate routes.

3. Topology Hiding

    - Visibility: BGP provides reachability information (Network Layer Reachability Information - NLRI) without exposing the internal topology of an AS.

    - Example: If AS 10000 (R1, R2, R3) connects to AS 20000, BGP only tells AS 20000: "I can reach network 192.168.1.0/24." It hides the internal links and hops between R1, R2, and R3.

4. Triggered vs. Periodic Updates

    - Triggered Updates: BGP only sends updates when a route changes or is withdrawn. It does not periodically send the entire routing table.

    - Maintenance: In a stable state, BGP peers only exchange small Keepalive messages (default: 60 seconds).

    - Contrast: Protocols like RIP or OSPF require periodic full updates or LSA refreshes.

5. Policy-Based Path Selection

    - Selection Logic: BGP does not use a simple "cost" or "metric." Instead, it uses a complex Path Selection process based on Path Attributes (PA).

    - Key Attributes: AS-Path, Local Preference, MED, Community, etc.

    - Example: OSPF selects the path with the lowest link cost; BGP might select a path because it has a shorter AS-Path or a higher Local Preference assigned by the administrator.

**Autonomous System Numbers (ASN)**

IANA (Internet Assigned Numbers Authority) and the IAB (Internet Architecture 
Board) oversee the global distribution of IP addresses and ASNs.

*Note: AS 0 and AS 65535 are reserved and generally not usable for traffic.*