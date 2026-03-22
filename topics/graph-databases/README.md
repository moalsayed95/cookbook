# Graph Databases

## What is a Graph Database?

A graph database stores data as **nodes** (entities) and **edges** (relationships) instead of rows and columns. This makes it natural to model and query highly connected data — social networks, recommendation engines, fraud detection, knowledge graphs — where the relationships between things matter as much as the things themselves.

Traditional relational databases require expensive JOIN operations to traverse relationships. Graph databases make traversals a first-class operation, so queries like "find all friends-of-friends who bought X" run in constant time per hop rather than blowing up with table size.

**Key concepts:**
- **Node** — an entity (person, product, account)
- **Edge** — a relationship between two nodes (FOLLOWS, PURCHASED, KNOWS)
- **Property** — key-value data attached to nodes or edges
- **Label** — a tag that groups nodes by type

## Popular Graph Databases

- **Neo4j** — the most widely adopted, uses the Cypher query language
- **Amazon Neptune** — managed graph DB on AWS, supports Gremlin and SPARQL
- **ArangoDB** — multi-model (graph + document + key-value)
- **Memgraph** — in-memory graph DB optimized for real-time streaming

## Resources

### YouTube Videos
- [Intro to Graph Databases (Series)](https://www.youtube.com/watch?v=F-bwn8p3Pes&list=PL9Hl4pk2FsvWM9GWaguRhlCQ-pa-ERd4U&index=1)
- [Dgraph Graph Database in 100 Seconds](https://www.youtube.com/watch?v=OzDG68VvPxY)

### Articles & Docs
- [Neo4j Getting Started](https://neo4j.com/docs/getting-started/)
- [Graph Databases for Beginners (Neo4j)](https://neo4j.com/blog/why-graph-databases-are-the-future/)
