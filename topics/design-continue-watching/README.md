# Designing Netflix's "Continue Watching"

## The Interview Question

> "Design Netflix's Continue Watching feature."

The instinct: "Easy — every second, the frontend sends the user's timestamp and we update a row in our SQL database."

```sql
UPDATE watch_progress
SET position_seconds = 1247, last_watched_at = NOW()
WHERE user_id = 42 AND show_id = 'stranger-things-s4e1';
```

Then the kill-shot:

> "Netflix has ~250 million subscribers. If even 1% are streaming right now, that's 2.5 million writes per second hitting your database. Your SQL server has been on fire for three seconds."

The whole answer collapses. Because a relational database, no matter how tuned, was never designed to absorb millions of tiny upserts per second. Every write needs an ACID transaction, a row lock, an index update, a WAL flush — and the bottleneck isn't your code, it's the laws of physics.

This is the interview question that tests whether you understand **how databases scale horizontally** — and the single concept at the heart of it: **partitioning.**

---

## Why SQL Loses

Let's count the writes:

```
250M subscribers
× ~5% concurrent at peak     →   12.5M active streams
× 1 progress update / sec    →   12.5M writes / sec
```

A single Postgres instance handles maybe ~10,000 writes per second on a great day. You're asking it to handle **1,000× more**. You can't fix this with a bigger box — the entire shape of the problem is wrong for a single relational database.

What you actually need is a database that **splits the writes across thousands of machines automatically**. That's what NoSQL databases like Azure Cosmos DB, DynamoDB, and Cassandra do — and the mechanism they use is called **partitioning**.

---

## What Is a Partition? — The Mailroom Analogy

This is the concept everything else in this design hangs on. Get this and the rest is obvious.

Imagine your database is a **mailroom in a giant office building with 1,000 workers**. Every time a piece of mail arrives, *one specific worker* handles it — based on a sorting rule you decide up front. That rule is your **partition key**.

Each worker is a **partition** — their own desk, their own pile, their own throughput. They work in parallel. The mailroom as a whole can handle 1,000× what one worker could do alone.

The catch: the sorting rule determines whether the load spreads evenly or piles up.

**Bad rule: "Sort by sender."**

If 99% of the mail is from Amazon, *one* poor worker handles all the Amazon packages while the other 999 sit idle. That one worker drowns. The mailroom looks like it has 1,000 workers, but it performs like it has 1. **This is a hot partition.**

**Good rule: "Sort by recipient apartment number."**

Every worker gets a steady trickle from their assigned range of apartments. No one drowns. Load is evenly distributed. The mailroom actually performs like it has 1,000 workers.

That's it. That's partitioning.

| In the analogy | In the database |
|---|---|
| The mailroom | Your NoSQL database |
| One worker | One physical partition (a machine + storage slice) |
| The sorting rule | Your partition key |
| Each piece of mail | One row (one write) |
| One worker drowning | A hot partition — throttling, timeouts, errors |

**The partition key is the single most important decision you make when designing a NoSQL schema.** Pick wrong, and one worker dies. Pick right, and you can handle 12.5 million writes per second.

---

## Now Pick the Partition Key

For Continue Watching, every write is *"user X is at second Y of show Z."* Two candidates for the partition key:

### Wrong Choice — `show_id`

```
Partition key:  show_id  ("stranger-things-s4e1")
```

What happens when *Stranger Things* season 5 drops? Five million people start streaming the same episode within the first hour. Every single one of their progress updates maps to **the same partition key**, which means **the same worker**. That one worker is now handling 5M writes/sec. Throttled. Dead. The feature breaks for everyone watching the show.

This is the **trending content** trap. Any partition key tied to *what's being watched* will collapse the moment something goes viral.

### Right Choice — `user_id`

```
Partition key:  user_id  (42)
```

Now every user's writes go to *their own* worker (well, their own partition — multiple users share a worker, but each user's load is tiny). User 42 generates 1 write/sec. User 43 generates 1 write/sec. Spread across 250 million users, the writes distribute evenly across thousands of partitions. **No single worker is ever overwhelmed**, even when half the world is watching the same show.

The deep insight: **partition by the entity whose writes are independent**, not by the entity that creates correlation. Users watch independently. Shows create correlated traffic. Therefore partition by user.

---

## The Data Shape

The actual row in Cosmos DB / DynamoDB:

```json
{
  "userId": "42",                        ← partition key
  "showId": "stranger-things-s4e1",      ← row key within the partition
  "positionSeconds": 1247,
  "episodeId": "S04E01",
  "lastWatchedAt": "2026-05-31T18:34:12Z",
  "deviceId": "ios-iphone-15"
}
```

One row per (user, show). When you upsert, the database routes the write by the partition key — user 42's writes always land on the same worker, instantly.

---

## Reading — The Homepage Load

When you open Netflix, the homepage needs your "Continue Watching" carousel. The query:

```
GET all rows WHERE userId = 42
```

This is a **single-partition query** — the database routes directly to user 42's worker, reads back every show they're in the middle of (usually <20 rows), and returns. No scatter-gather. No cross-partition coordination. Sub-10ms reads, no matter how big the database gets.

This is the second reason `user_id` is the right partition key: it makes the most common query (load the carousel) a direct lookup.

---

## The Full Picture

```
                    ┌──────────────────────────────────────────────┐
                    │           NoSQL Database (Cosmos DB)         │
   12.5M writes/sec │                                              │
   ───────────────▶ │  hash(user_id)  →  pick partition            │
                    │                                              │
                    │   ┌─────────┐  ┌─────────┐       ┌─────────┐ │
                    │   │ Worker 1│  │ Worker 2│  ...  │Worker N │ │
                    │   │ users:  │  │ users:  │       │ users:  │ │
                    │   │ 1, 1001,│  │ 2, 1002,│       │  N,…    │ │
                    │   │ 2001…   │  │ 2002…   │       │         │ │
                    │   └─────────┘  └─────────┘       └─────────┘ │
                    │                                              │
                    │   each worker handles ~12.5M / N writes/sec  │
                    └──────────────────────────────────────────────┘
```

With N=1,000 workers, every worker handles 12,500 writes/sec — entirely manageable. Add more users? Add more workers. The system scales linearly.

---

## Production Considerations

| Decision | What to think about |
|---|---|
| **How often to write** | Every *second* is overkill. Real Netflix writes ~every 10–30 seconds plus on pause/exit. Cuts the load by 10–30×. |
| **Buffer at the edge** | The video player can hold progress in local state and only flush to the backend periodically. Network blips don't lose much progress. |
| **TTL for old rows** | If a user hasn't touched a show in 90 days, it shouldn't be in "Continue Watching." Set a TTL on the row and let the database expire it automatically. |
| **Don't use SQL for the *write* path** | SQL can still own the user account, billing, the catalog. Just not the high-throughput playback state. Use the right tool per write pattern. |
| **Read replicas in user regions** | A user in Tokyo shouldn't read their progress from US-East. Cosmos DB / DynamoDB Global Tables replicate per region — pair with [CDN Anycast Routing](../cdn-anycast-routing/) for the API hop. |
| **Watch out for power users** | A single user with 500 in-progress shows isn't a hot partition exactly, but a "fat partition" is its own problem. Set a max — Netflix caps the carousel at ~20 shows. |

---

## The Key Insight

NoSQL doesn't scale because it's magic. It scales because it **shards your data across many machines, and lets you pick the rule for how to shard it**.

That rule — the partition key — is the most important schema decision you make. Pick a key correlated with what *every user is doing right now* (a trending show, the current hour, a popular country) and you funnel all traffic to one worker. Pick a key tied to *who's doing the work independently* (the user) and the load spreads across the whole fleet.

The whole architecture of Continue Watching collapses to one decision: **partition by user, not by show.**

---

## TL;DR

- **Don't use SQL for high-frequency state updates** — millions of per-second writes overwhelm a single relational database.
- **A partition is one machine + storage slice** that handles a portion of your data. A **partition key** is the rule the database uses to decide which partition owns each row.
- **Hot partition** = one worker drowning while the rest sit idle. Caused by a partition key correlated with what's currently popular.
- For Continue Watching, **partition by `user_id`**. Each user writes independently (~1 write per N seconds), so the load distributes evenly even when everyone watches the same trending show.
- **Reads by `user_id`** are single-partition lookups — sub-10ms regardless of total database size.
- **Tune the write rate** (every 10–30s, not every second), buffer at the edge, set TTLs on stale rows, and use SQL for the things SQL is good at (accounts, billing, catalog).

When the interview asks "design Continue Watching," the answer isn't "Cosmos DB" or "DynamoDB." It's **"User ID as the partition key, because the writes are independent per user and the reads are scoped per user."** That sentence is the whole design.

---

## Related

- [Designing Google Drive](../design-google-drive/) — another "designing X" piece where the right choice is to *not* use SQL for the heavy work
- [Composite Indexes — The Multi-Column Index Trap](../composite-indexes/) — same theme, different layer: the schema must match the query
- [CDN Anycast Routing](../cdn-anycast-routing/) — once your data layer scales, the network is the next bottleneck

---

## Resources

### Docs
- [Azure Cosmos DB — Partitioning and horizontal scaling](https://learn.microsoft.com/azure/cosmos-db/partitioning-overview)
- [Azure Cosmos DB — Choose a good partition key](https://learn.microsoft.com/azure/cosmos-db/partitioning-overview#choose-partitionkey)
- [DynamoDB — Best practices for designing partition keys](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/bp-partition-key-design.html)
- [Cassandra — Data modeling and partition keys](https://cassandra.apache.org/doc/latest/cassandra/data_modeling/intro.html)
