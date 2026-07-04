# Sharing localhost — Get Your `localhost:3000` on the Internet

## The Interview Question

> "How can I share my localhost with someone without deploying my app?"

You send a friend `http://localhost:3000`, they open it, and they see… nothing. Or their *own* broken page. Understanding *why* that link is useless to them is the whole lesson — and the fix takes one command.

---

## Why the Link You Sent Is Broken

`localhost` means **"this computer, talk to myself."** It always resolves to `127.0.0.1` — the machine the browser is running on.

So when your friend opens `localhost:3000`, their browser doesn't call *your* laptop. It calls *their* laptop, on port 3000, where nothing is running. They knock on their own door and find an empty room.

```
You send:   http://localhost:3000

Your machine                     Friend's machine
┌──────────────┐                 ┌──────────────┐
│ app on :3000 │  ← NOT this     │  nothing :(  │  ← their browser
│ 127.0.0.1    │                 │  127.0.0.1   │     goes here
└──────────────┘                 └──────────────┘
```

Your app is a program **listening on your machine only**. It was never on the internet — so there's no public address for anyone else to reach.

---

## Two Ways to Fix It

| | Tunneling | Deployment |
|---|---|---|
| **Where the app runs** | Still on your laptop | On a cloud server |
| **Public address** | Temporary tunnel URL | Real, permanent domain |
| **Your machine must be on** | Yes — close the laptop, link dies | No — server is always on |
| **Setup time** | One command, seconds | Minutes to hours |
| **Best for** | Demos, interviews, webhooks, quick feedback | Real users, production, 24/7 |

**Pick based on how long the link needs to live.** Need it for the next 20 minutes? Tunnel. Need it for the next 20 months? Deploy.

---

## Option 1: Tunneling (Temporary)

A **tunnel** creates a public URL that forwards traffic straight to your local port. The app stays on your machine; the tunnel is a bridge from the internet to `localhost:3000`.

```
Internet ──► https://abc123.ngrok.app ──► [tunnel] ──► your laptop :3000
```

You run one command and your laptop suddenly has a shareable link:

```bash
# ngrok — the classic
ngrok http 3000

# Cloudflare Tunnel — free, no signup for quick tunnels
cloudflared tunnel --url http://localhost:3000

# Zero-install, works over SSH
ssh -R 80:localhost:3000 localhost.run
```

Any of these prints a public `https://…` URL. Send *that* — not `localhost` — and your friend reaches the app running on your machine.

**Why it's perfect for demos and interviews:** instant, HTTPS by default, and nothing leaves your laptop. **Why it's temporary:** the moment you close the tunnel or shut the laptop, the link dies — and free tunnels hand you a new random URL each time.

> The other killer use case: **testing webhooks.** Stripe, GitHub, or Twilio need a public URL to POST events to. A tunnel points them straight at your local dev server so you can debug the handler live.

---

## Option 2: Deployment (Permanent)

**Deployment** moves your app off your laptop onto a **cloud server that's always on.** Now a remote machine answers requests, and it has a real public address, so anyone in the world can reach it anytime — whether your laptop is open or in a drawer.

```
Internet ──► https://myapp.com ──► cloud server (always on) :3000
```

Modern platforms make this nearly as fast as a tunnel:

```bash
vercel          # frontends / Next.js
railway up      # full-stack apps + databases
fly deploy      # containers, close to your users
```

This is the answer when you have **real users**. It's stable, it survives reboots, and it scales — but it's a genuine deploy, not a bridge back to your desk.

---

## The One Thing to Remember

**Tunneling shares the app *on your laptop*. Deployment *moves* the app to a server.**

A tunnel is a temporary bridge from the internet to your machine — the app never leaves your desk, and the link dies when you do. Deployment relocates the app to an always-on server with a permanent address.

---

## TL;DR

- `localhost` means "this computer" — the link is useless to anyone else because their browser talks to *their* machine.
- **Tunneling** (`ngrok`, `cloudflared`, `localhost.run`) = one command, instant public URL to your laptop. Great for demos, interviews, and webhook testing. Dies when you close it.
- **Deployment** (`vercel`, `railway`, `fly`) = move the app to an always-on cloud server with a permanent domain. The answer for real users.
- Rule of thumb: **temporary share → tunnel. Permanent home → deploy.**

---

## Resources

### Docs
- [ngrok — Getting Started](https://ngrok.com/docs/getting-started/)
- [Cloudflare Tunnel](https://developers.cloudflare.com/cloudflare-one/connections/connect-networks/)
- [localhost.run](https://localhost.run/)
