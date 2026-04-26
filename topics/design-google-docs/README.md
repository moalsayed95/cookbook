# Designing Google Docs

## The Interview Question

> "How would you design Google Docs?"

It sounds simple — a text editor in the browser. The hard part is the one feature everyone takes for granted: **multiple people editing the same document at the same time, in real time, without their changes stomping on each other.**

Most of the rest (titles, permissions, comments, version history) is standard CRUD. The real interview is about **real-time collaborative editing**.

## What's Actually Happening in the Browser

Open a Google Doc, share it, and load it in two tabs. In the network panel you'll see a single **long-running connection** that never closes. As you type, small messages stream back and forth over that one connection — not a new HTTP request per keystroke.

Google uses **QUIC** under the hood (they invented it). For a system design interview, **WebSockets** do the same job conceptually: a persistent, bidirectional channel between client and server.

## Requirements

### Functional

- Create, read, update, delete documents (CRUD)
- **Multiple users can edit the same document concurrently**
- Updates show up in **real time** for everyone in the doc
- Show each user's **cursor position** (helps avoid stepping on each other)

Out of scope for the interview: auth, comments, permissions, sharing, offline mode.

### Non-Functional

- Up to **100 concurrent users per document** (this is what real Google Docs allows)
- Update latency **≤ 200ms** between users
- Documents are durable
- All clients must **converge to the same state** — no permanent conflicts

The user count and document count can be in the millions, but that's not the interesting bottleneck. The interesting bottleneck is the concurrent editing of a single doc.

## High-Level Architecture

Two services behind an API gateway:

- **Document Service** — HTTP. Handles create / delete / metadata / fetching the document body.
- **Edit Service (WebSocket)** — Handles real-time edits and broadcasts them to everyone in the same document.

Storage:

- **Object Store + CDN** — for the document body itself. Average doc is ~100 KB but some are huge, so blobs make more sense than a relational row.
- **Database (Cassandra)** — for the stream of edits. Write-heavy, so a wide-column store fits well.

A WebSocket service can sit behind an API gateway just like an HTTP service — same URL prefix, different protocol, different backend.

## The Core Problem: How Do You Send an Edit?

### Option 1: Send the whole document on every change

Terrible. A 100 KB blob over the wire every keystroke. Object stores can't patch files in place either — you'd rewrite the entire blob.

### Option 2: Send only the edits (deltas)

Much better. Tiny payloads. But this introduces **conflicts**.

Picture this string:

```
hello!
0 1 2 3 4 5
```

Two users, almost simultaneously:

- User A: `insert "," at position 5`
- User B: `insert " world" at position 5`

The server applies A first → `hello,!`. Now position 5 is the `!`, not what User B was pointing at. Apply B as-is and you get `hello, world!` in the wrong spot.

This is the **conflict problem**. Sending the whole doc has the same issue, just more expensive.

### Option 3: Operational Transform (OT)

OT takes incoming edits and **transforms them against edits that already happened** so the final state is consistent and matches each user's intent.

In the example above, when B's edit arrives the server sees A already inserted one character at position 5, so it shifts B's position from 5 to 6. Result: `hello, world!`.

OT runs on **both sides**:

- **Server side** — transforms a new edit against earlier edits before broadcasting.
- **Client side** — when a remote edit arrives, transform it against any local edits the client already applied.

OT is non-trivial to implement correctly (think LeetCode Hard, but with way more edge cases). For an interview, you don't need to code it — you need to know it exists, why it exists, and where it sits in the architecture.

> Alternatives worth knowing by name: **Last-Write-Wins** (simpler, worse), and **CRDTs** (conflict-free replicated data types — more modern, more complex). Google Docs originally used OT.

## Ordering the Edits

Client clocks are unreliable (offline users, clock skew). Use the **server as the source of truth for ordering** — edits are sequenced in the order the WebSocket service receives them.

## Reads, Writes, and Compaction (the Hybrid Storage Trick)

Updating the object store on every keystroke is too slow. So:

- **Edits go to the database** (Cassandra), not the object store.
- The object store holds a **snapshot** of the document — possibly stale.
- The newest changes live as a stream of edits in the DB on top of that snapshot.

### Loading a document

1. Fetch the snapshot from the object store (via CDN — fast).
2. Fetch any newer edits from the database.
3. Apply those edits locally → you have the latest state.

### Live editing

1. Edit goes over WebSocket to the Edit Service.
2. Edit Service runs OT, writes the edit to the database, broadcasts to other clients in the same room.

### Compaction

When the **last user disconnects** from a document (room size drops to zero):

1. Edit Service publishes a message to a queue.
2. A **compaction worker** picks it up.
3. The worker reads the snapshot + pending edits, applies them, writes a new snapshot to object storage.
4. The compacted edits can be deleted (or tombstoned if you want version history).

This gives you the best of both worlds: cheap fast snapshots from object storage + low-latency incremental edits from the DB.

## Scaling the WebSocket Layer

Stateless services (Document Service, etc.) scale trivially — just add instances behind the load balancer.

WebSockets are **stateful**. Every user editing the same document **must connect to the same WebSocket instance**, otherwise the broadcast breaks.

Solution: route by `documentId`. All users for a given document hash to the same instance. **Consistent hashing** handles instance failures gracefully — when a node dies, only the documents it owned get redistributed.

## Things You Could Mention If You Have Time

- **Client-side debouncing / batching** — don't send 30 edits per second per user.
- **Versioning** — keep edits around (tombstoned) for history and undo.
- **CRDTs** — alternative to OT; more complex but no central ordering authority needed.
- **Cursor presence** — small ephemeral state piggybacked over the same WebSocket so users see each other's cursors.

## TL;DR

- Real-time editing = persistent connection (WebSocket / QUIC).
- Don't send whole documents — send small **edits**.
- Edits collide → use **Operational Transform** to keep all clients consistent.
- Use **server order** as the source of truth.
- Store snapshots in **object storage**, edits in a write-optimized **database**, and **compact** when the room is empty.
- Scale WebSockets by **routing on document ID** with consistent hashing — every collaborator on the same doc must land on the same instance.
