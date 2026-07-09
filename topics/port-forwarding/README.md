# Port Forwarding

## The Interview Question

> "Your friend wants to join your Minecraft server running on your laptop. You give them your IP address. Why can't they connect?"

Most people jump to "firewall" — and they're half right. But the real answer is architectural: your laptop doesn't *have* a public IP address. It sits behind a router, on a private network that the internet can't see. Port forwarding is how you punch a hole through that wall — and understanding why it sometimes *can't* work anymore is the part nobody explains.

---

## The Receptionist Analogy

Think of your home router as a **receptionist at a front desk**.

Your home has one public address — that's the building. Inside, you've got rooms: your laptop is Room 201, your phone is Room 304, your smart TV is Room 105. Nobody on the street knows which room is which. All they see is the front door.

When someone knocks on the front door (sends traffic to your public IP), the receptionist has to decide: *which room do I send this person to?* Without instructions, the receptionist turns them away. "Nobody's expecting you."

**Port forwarding is the set of instructions you leave at the front desk.** You tell the receptionist: "Anyone who asks for Room 25565 — send them straight to the laptop in Room 201." Now your friend knocks, says "port 25565," and the receptionist guides them right to your machine.

---

## How It Actually Works

Every device on your home network gets a **private IP address** — something like `192.168.1.x`. These addresses are invisible from the internet. They only work inside your home.

Your router, meanwhile, holds the **one public IP address** your ISP assigned you. When your laptop makes a request to the outside world, the router swaps the private source address for the public one (this is NAT — Network Address Translation) and remembers who asked, so it can route the response back.

```
┌─────────────────────────────────────────────────────────┐
│                    The Internet                          │
│                                                         │
│           Your Public IP: 84.92.155.12                  │
└──────────────────────────┬──────────────────────────────┘
                           │
                    ┌──────┴──────┐
                    │   Router    │  ← the receptionist
                    │  (NAT/FW)  │
                    └──┬────┬────┘
                       │    │
          ┌────────────┘    └────────────┐
          │                              │
   ┌──────┴──────┐               ┌──────┴──────┐
   │   Laptop    │               │    Phone    │
   │ 192.168.1.5 │               │ 192.168.1.8 │
   │  :25565     │               │             │
   └─────────────┘               └─────────────┘
```

**Without a port-forwarding rule:** your friend sends a packet to `84.92.155.12:25565`. It hits the router. The router has no idea which internal device wants traffic on that port. Packet dropped. Connection refused.

**With a port-forwarding rule:** you log into the router and add: *"External port 25565 → forward to 192.168.1.5:25565."* Now the router knows exactly where to send it. The receptionist has her instructions.

---

## Public vs Private IPs — The Key Distinction

| | Public IP | Private IP |
|---|---|---|
| **Who assigns it** | Your ISP | Your router (via DHCP) |
| **Visible from the internet** | Yes | No |
| **Unique globally** | Yes (in theory) | Only unique inside your home |
| **Example** | `84.92.155.12` | `192.168.1.5`, `10.0.0.23` |
| **Who has it** | Your router (one per household) | Every device behind the router |

**Your laptop is hidden.** It can *reach out* to the internet (the router remembers and routes replies back), but nobody on the internet can *reach in* to it directly — unless the router has explicit forwarding instructions.

---

## Why Port Forwarding Breaks: CGNAT

Here's where most tutorials stop. But the real world threw a wrench into this.

IPv4 addresses ran out. There are only ~4.3 billion, and we've used them all. So ISPs started doing something brutal: they put **hundreds of homes behind a single public IP address**, using a massive router they control. This is called **CGNAT** — Carrier-Grade NAT.

```
┌───────────────────────────────────────────────────┐
│                  The Internet                      │
│                                                   │
│          Shared Public IP: 100.64.0.1             │
└────────────────────────┬──────────────────────────┘
                         │
              ┌──────────┴──────────┐
              │   ISP's Giant Router │  ← you DON'T control this
              │       (CGNAT)        │
              └───┬─────┬─────┬─────┘
                  │     │     │
           Home A   Home B   Home C
           (you)
                  │
           ┌──────┴──────┐
           │ Your Router  │  ← you control this, but it's too late
           └──────────────┘
```

You're now **double-NAT'd**. You can set up port forwarding on *your* router all you want — it doesn't matter. Traffic from the internet hits the ISP's router first, and you can't add rules there. You don't own it.

**How to tell if you're behind CGNAT:** compare the "WAN IP" your router reports with what a site like `whatismyip.com` shows. If they're different, you're behind CGNAT. Your router's "public" IP is actually just another private address inside the ISP's network.

---

## The Fix: Tunneling

When CGNAT blocks you, port forwarding is physically impossible. But the goal — *let someone on the internet reach a service on my machine* — still has a solution. You just need to flip the direction.

Instead of waiting for inbound traffic, your machine **reaches out** to a relay server on the public internet and keeps the connection open. Now anyone who contacts that relay gets forwarded through the already-open connection back to your machine. Traffic flows *out* to get *in*.

```
Your laptop ──outbound──► Relay server (public IP) ◄── your friend connects here
             tunnel stays open, traffic flows both ways
```

This is exactly what tools like **ngrok**, **Cloudflare Tunnel**, and **Tailscale** do:

| Tool | Best for | How it works |
|---|---|---|
| **ngrok** | Quick demos, webhook testing | Gives you a temporary public URL |
| **Cloudflare Tunnel** | Persistent self-hosting | Free, no port forwarding needed, runs as a daemon |
| **Tailscale** | Connecting your own devices | Creates a private mesh VPN using WireGuard |

**The key insight:** tunneling doesn't require port forwarding *or* a public IP. It works behind CGNAT, behind firewalls, behind anything — because the connection is initiated *outward* by your machine, and outbound connections always work.

---

## When Do You Still Need Port Forwarding?

### ✅ Port forwarding works when

| Scenario | Why |
|---|---|
| You have a real public IP from your ISP | No CGNAT — your router is the front door |
| You're self-hosting a game server at home | Persistent, fast, no relay latency |
| You control the router (home network) | You can add the forwarding rule |

### ❌ Port forwarding won't help when

| Scenario | Use instead |
|---|---|
| You're behind CGNAT | Tunneling (ngrok, Cloudflare Tunnel) |
| You're on a university/corporate network | Tunneling or VPN |
| You need a stable public URL | Deploy to a cloud server or use Cloudflare Tunnel |
| You want zero config | Tailscale (no router changes needed) |

---

## TL;DR

- **Port forwarding is a rule on your router** that says "traffic on this port goes to this internal device." Without it, inbound traffic gets dropped — nobody knows which device you mean.
- **It only works when you control the first public-facing router.** If your ISP puts you behind CGNAT (and many do), your router isn't public-facing anymore — so your rules are useless.
- **Check for CGNAT** by comparing your router's WAN IP to `whatismyip.com`. Different? You're double-NAT'd.
- **When blocked, tunnel out.** Tools like ngrok, Cloudflare Tunnel, and Tailscale flip the direction — your machine reaches out to a public relay, and traffic flows back through. No port forwarding needed.
- **Default recommendation:** try port forwarding first (it's the simplest path). If it doesn't work, assume CGNAT and reach for a tunnel.

---

## Related

- [Sharing localhost](../share-localhost/) — tunneling tools in action (ngrok, cloudflared, localhost.run)
- [VPN vs Proxy](../vpn-vs-proxy/) — how VPNs create private tunnels across the internet
- [HTTP vs HTTPS](../http-vs-https/) — what happens to the data inside that tunnel

---

## Resources

### YouTube
- [Port Forwarding Explained — PowerCert](https://www.youtube.com/watch?v=2G1ueMDgwxw)
- [NAT and CGNAT Explained — NetworkChuck](https://www.youtube.com/watch?v=qij5qpHcbBk)

### Docs
- [What is CGNAT? — Cloudflare](https://www.cloudflare.com/learning/network-layer/what-is-cgnat/)
- [Cloudflare Tunnel — Zero Trust](https://developers.cloudflare.com/cloudflare-one/connections/connect-networks/)
- [Tailscale — How it works](https://tailscale.com/blog/how-tailscale-works)
