**Evolution of BGP**

- 1980s: EGP (Exterior Gateway Protocol) was introduced as the initial inter-AS routing protocol.

- 1989: BGP-1 was released.

- Current Standard: BGP-4 is the dominant version.

- BGP-4+ (Multiprotocol BGP / MP-BGP): An extension of BGP-4 that supports multiple address families (AFI/SAFI). While BGP-4 only supports IPv4, MP-BGP adds support for IPv6, VPNv4, VPNv6, and L2VPN.

*BGP is a Path Vector routing protocol designed to achieve reachability between Autonomous Systems (AS) and to select the optimal path based on attributes.*

**Key Characteristics**

- Reliable Transport: BGP uses TCP port 179. BGP sessions are established only after a successful TCP three-way handshake.

- Incremental Updates: BGP uses triggered (incremental) updates rather than periodic updates, reducing unnecessary control plane traffic.

- High Scalability: Designed to carry massive amounts of routing information (the current global Internet routing table exceeds 900k+ prefixes).

- Rich Policy Control: Provides extensive attributes and routing policies to influence path selection and control how routes are advertised to peers.

- MPLS/VPN Support: Acts as the control plane for MPLS L3VPN, carrying customer VPN labels and prefixes.

- Stability Features:

    1. Route Aggregation: Reduces routing table size.

    2. Route Dampening: Prevents network instability caused by "route flapping" (frequent prefix withdrawal and re-advertisement).

**BGP Roles and Terminology**

- BGP Speaker: Any router running the BGP process.

- BGP Peers (Neighbors): Two BGP speakers that have established a BGP session and are exchanging routing information.

- Incremental Signaling: Peers only exchange new or modified routing information (Network Layer Reachability Information - NLRI) once the initial full table sync is complete.

**BGP Security and Authentication**

- Common BGP Attacks

    1. Unauthorized Peering: Establishing an illegal BGP neighbor relationship to inject malicious routes or intercept traffic.

    2. DoS/Resource Exhaustion: Flooding a router with spoofed BGP packets to force high CPU utilization, potentially crashing the BGP process.

Security Mechanisms

BGP uses two primary methods to secure neighbor interactions: Authentication and GTSM.

1. Authentication

    - MD5 Authentication: Used during the TCP connection establishment. The MD5 password is set for the TCP session, and the TCP stack handles the verification. This prevents unauthorized TCP hijacking.

    - Keychain Authentication: A more flexible method allowing for hitless password rotation over time.

        Note: While Keychain is a standard concept, specific implementations (like those mentioned in Huawei documentation) may have proprietary characteristics compared to Cisco or Juniper.

    - Configuration Impact: BGP authentication often requires a Hard Reset (clearing the BGP session) to take effect if the session was already established before the password was configured.

        Modern BGP implementations often support **Route Refresh** (Soft Reset), but changes to authentication or Peer IP still require a hard  reset.
    
2. GTSM (Generalized TTL Security Mechanism)

GTSM protects the CPU from packet-flooding attacks by verifying the TTL (Time to Live) value of incoming BGP packets. Since EBGP peers are typically directly connected, any packet with a TTL significantly lower than 255 is flagged as potentially forged and discarded.

- **BGP Message Exchange Process**

    1. TCP Three-Way Handshake: Establishing the transport layer connection.

    2. Open Message: Exchange of BGP version, ASN, Hold Time, and BGP Identifier (Router ID).

    3. Update Message: Advertisement of new routes or withdrawal of unreachable routes.

    4. Keepalive Message: Periodic messages to maintain the session (default 60s).

    5. Notification Message: Sent when an error is detected, followed by the immediate closure of the BGP connection.