# UUID — Universally Unique Identifier

## Resources

### YouTube Videos
- [UUIDs vs Serial for Primary Keys — 5mins of Postgres E59](https://www.youtube.com/watch?v=TSw0Jozx7Lw&t=314s)

### Docs
- [UUID — Python Docs](https://docs.python.org/3/library/uuid.html)
- [UUID Data Type — PostgreSQL Docs](https://www.postgresql.org/docs/current/datatype-uuid.html)

---

## What is a UUID?

A UUID (Universally Unique Identifier) is a 128-bit, randomly generated ID used to uniquely identify a record — a user, an order, a file, anything.

It looks like this:

```
550e8400-e29b-41d4-a716-446655440000
```

Five groups of hex characters separated by dashes: `8-4-4-4-12`.

Obviously built for machines, not humans — and that's the point.

## Why Not Just Use 1, 2, 3?

Sequential IDs (auto-increment) work fine when you have **one** database on **one** server. The problem starts when you scale.

If two servers both create "User 42" at the same time, you now have **duplicates and broken data**.

UUIDs solve this. The chance of two machines generating the same UUID is practically zero — even if millions of machines are generating IDs at the same time.

## Quick Example

A user signs up on your website. Your backend generates a UUID and saves it as their ID:

```python
import uuid

user_id = uuid.uuid4()
print(user_id)  # e.g. 7c9e6679-7425-40de-944b-e07fc1f90ae7
```

That's it. No need to check if the ID already exists. No need to coordinate with other servers.

## UUID Versions

Not all UUIDs are created equal:

| Version | How it's generated | When to use it |
|---------|-------------------|----------------|
| **v1** | Based on timestamp + MAC address | When you need time-ordering but don't mind leaking hardware info |
| **v4** | Completely random | The most common choice — just give me a unique ID |
| **v5** | Based on a namespace + name (SHA-1 hash) | When the same input should always produce the same UUID |
| **v7** | Timestamp-ordered + random (newer spec) | When you want UUID randomness **and** sortable by creation time |

**v4** is by far the most widely used. When someone says "UUID" they usually mean UUIDv4.

## UUID vs Auto-Increment (Serial)

This is the real debate when choosing primary keys for your database:

| | Auto-Increment (Serial) | UUID |
|---|---|---|
| **Format** | `1, 2, 3, 4 …` | `550e8400-e29b-41d4-a716-…` |
| **Size** | 4–8 bytes | 16 bytes |
| **Readability** | Human-friendly | Machine-friendly |
| **Uniqueness** | Unique per table | Unique globally |
| **Distributed systems** | Breaks without coordination | Works everywhere independently |
| **Index performance** | Great — sequential inserts are fast | Slower — random values fragment indexes |
| **Guessable** | Yes — `/users/42` → try `/users/43` | No — impossible to predict the next ID |
| **Merging databases** | Collisions guaranteed | No collisions |

### When Serial Wins
- Single database, single server
- You need fast sequential inserts and compact indexes
- Internal IDs that users never see

### When UUID Wins
- Distributed systems with multiple servers or databases
- IDs exposed in URLs or APIs (security — can't guess the next one)
- Microservices that generate IDs independently
- You ever plan to merge data from multiple sources

### The Best of Both Worlds

Many teams use **UUIDv7** — it's random enough to avoid collisions but time-ordered so your database indexes stay efficient. PostgreSQL 17+ has native `uuidv7` support.

Another common pattern: use an **auto-increment integer** as the internal primary key for fast joins, and a **UUID** as the public-facing external ID.

```sql
CREATE TABLE users (
    id         SERIAL PRIMARY KEY,
    public_id  UUID DEFAULT gen_random_uuid() UNIQUE,
    email      TEXT NOT NULL
);
```

Internal queries use `id` (fast). APIs and URLs expose `public_id` (safe).

## TL;DR

A UUID is a collision-resistant, randomly generated identifier. Use it when creating records like users or orders so every entry stays globally unique — no coordination needed. Use auto-increment when you're on a single database and need raw speed. When in doubt, UUIDv7 or the dual-key pattern gives you the best of both worlds.
