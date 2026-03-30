# VPN vs Proxy

## Resources

### YouTube Videos
- [Proxy vs VPN — There's a BIG Difference](https://www.youtube.com/watch?v=VhLoxxOrwIo)

### Docs
- [How VPNs Work — Cloudflare](https://www.cloudflare.com/learning/access-management/what-is-a-vpn/)
- [What is a Proxy Server? — Cloudflare](https://www.cloudflare.com/learning/cdn/glossary/reverse-proxy/)

---

Both proxies and VPNs mask your IP address by rerouting your internet traffic through a remote server. That's where the similarities end.

## What is a Proxy?

A proxy sits between you and the internet, forwarding your requests through a different server so the destination sees the proxy's IP instead of yours.

Key characteristics:
- Works on the **application level** — it only reroutes traffic from the single app you configure it with (e.g. your browser)
- Usually **does not encrypt** your traffic
- Lightweight — because there's no encryption overhead, proxies tend to be faster

### Common Proxy Types

| Type | How it works |
|------|-------------|
| **HTTP Proxy** | Handles web traffic only (HTTP/HTTPS) |
| **SOCKS5 Proxy** | Handles any type of traffic (web, gaming, torrents) — more versatile |
| **Transparent Proxy** | The user doesn't even know it's there — often used by companies and schools to filter content |

## What is a VPN?

A VPN (Virtual Private Network) also routes your traffic through a remote server, changing your IP in the process. But it works fundamentally differently.

Key characteristics:
- Works on the **operating system level** — it redirects **all** of your traffic, whether it's from your browser, a background app, or anything else
- **Encrypts your data** before it leaves your device — scrambled so no third party can spy on your activity
- Creates an encrypted **tunnel** between your device and the VPN server

## Head-to-Head Comparison

| | Proxy | VPN |
|---|---|---|
| **Scope** | Single app | Entire device |
| **Encryption** | Usually none | Full encryption |
| **Speed** | Generally faster (no encryption overhead) | Slightly slower (encryption costs) |
| **Security** | IP masking only | IP masking + encrypted traffic |
| **Privacy** | Basic — traffic is still visible | Strong — traffic is scrambled |
| **Setup** | Per-app configuration | One toggle, system-wide |
| **Best for** | Changing IP quickly, lightweight tasks, gaming | Security, privacy, protecting all traffic |

## Security

VPN wins here. Your data gets encrypted before reaching the VPN server, meaning no one in between — not your ISP, not the coffee shop Wi-Fi owner, not anyone — can read your traffic.

A proxy just changes your IP. The traffic itself travels in plain text (in most cases), so anyone intercepting it can still see what you're doing.

## Privacy

Depends entirely on who's running it.

**Free proxies / free VPNs** — your data is likely being logged and sold. If you're not paying for the product, you are the product.

**Paid, reputable VPNs** — many have strict no-log policies backed by independent audits. They also often block trackers and ads.

**Paid proxies** — generally don't log, but also don't encrypt, so your ISP can still see your traffic.

## Speed

Proxies are generally faster because they skip the encryption step. If raw speed matters (like gaming or scraping), a proxy has less overhead.

VPNs add encryption, which takes a small performance hit. In practice, a good VPN on a nearby server is barely noticeable for normal browsing.

## So Which Should You Use?

**Use a VPN if you want:**
- Privacy and security across your entire device
- Encrypted traffic on public Wi-Fi
- To hide your browsing activity from your ISP
- To change your virtual location for all apps at once

**Use a proxy if you want:**
- To change your IP for a single app only
- Speed over security (gaming, scraping)
- A lightweight solution without encrypting everything
- To bypass a simple geo-block quickly

**Use both if you want:**
- A proxy for a specific app (e.g. a SOCKS5 proxy for gaming) while running a VPN for everything else

## TL;DR

A proxy changes your IP for one app. A VPN encrypts everything and changes your IP for your entire device. If security and privacy matter, go VPN. If you just need a quick IP change for one thing, a proxy works fine.
