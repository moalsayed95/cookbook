# How Tinder Finds Matches in Milliseconds

## The Problem

Tinder has over 75 million users worldwide. A naive approach — calculating the distance between you and every other user — would be impossibly slow. They need sub-second latency to make swiping feel instant.

## The Solution: Geospatial Indexing with Google's S2 Library

Instead of scanning the entire database, Tinder uses **geosharding** — partitioning users into geographic regions so queries only touch the data that's nearby.

The magic behind it is Google's **S2 Geometry Library**, which works in three steps:

### 1. Project the Earth onto a Cube

Flat maps (like Mercator projections) distort distances — Greenland looks the size of Africa. S2 avoids this by projecting the Earth's surface onto the six faces of a surrounding cube, preserving distance relationships far more accurately.

### 2. Trace a Hilbert Curve

Each cube face is then mapped using a **Hilbert Curve** — a space-filling curve that continuously folds and weaves across the surface, converting 2D coordinates into a 1D index. The key property: **points that are close on the map stay close on the curve**. This means a simple range query on the 1D index returns geographically nearby users.

### 3. Adaptive Cell Sizing

S2 divides the world into a hierarchy of **cells** (each cell splits into four smaller cells). Dense areas like New York City get smaller, more granular cells (~22.5 miles at Level 8), while rural areas use larger cells (~45 miles at Level 7). This keeps shard sizes balanced regardless of population density.

## How a Swipe Request Works

1. You open the app
2. The backend determines which **S2 cell** you're in
3. It queries only that shard and its neighboring shards — not the whole database
4. Matches are returned in a fraction of a second

Instead of scanning millions of users globally, the system narrows it down to two or three data shards. This geosharded approach lets Tinder handle **20x more computations** than their previous single-index architecture.

## Under the Hood

- **Elasticsearch** stores user data, geosharded across nodes
- **Apache Kafka** ensures write ordering — location updates are consistently hashed to specific partitions
- **Coordinating nodes** route queries to the right shards based on your location and distance filters
- **Randomized shard distribution** across servers balances load across time zones (so traffic spikes in one region don't overload specific nodes)

## Resources

### Articles
- [Design Tinder — System Design Handbook](https://www.systemdesignhandbook.com/guides/design-tinder/)
- [How Tinder Recommends to 75 Million Users — ByteByteGo](https://blog.bytebytego.com/p/how-tinder-recommends-to-75-million)
- [Geosharded Recommendations Part 1: Sharding Approach — Tinder Engineering](https://medium.com/tinder/geosharded-recommendations-part-1-sharding-approach-d5d54e0ec77a)
