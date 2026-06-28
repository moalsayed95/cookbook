# Vector Databases — A Storage Room of Floating Balloons

![A storage room as a database: each object is a balloon positioned by the meaning of its data — chair, sofa and table cluster together, cat and dog cluster apart — and each balloon's position is its vector embedding [0.3, 0.2, … 0.6]](vector-db-storage-room-analogy.png)

## The Interview Question

> "Why can't you just use your normal SQL database for search? Why reach for a vector database?"

A normal database finds **exact matches**. A vector database finds things **by meaning**. Once that difference clicks, the whole landscape — and which one to pick — falls into place.

---

## The Storage Room Analogy

Picture a database as a storage room living in a server. Normally you put objects on shelves and find them by an exact label: `chair.jpeg`.

A **vector database** arranges the same room differently. Every object becomes a **floating balloon**, and its position is decided by the *meaning* of the data. Add a chair and it drifts next to the sofa and the table — they're all furniture. The cat and dog float off in their own corner.

That position — the balloon's coordinates in the room — is the **embedding**: a long list of numbers like `[0.3, 0.2, … 0.6]`. That's the picture above, exactly.

---

## Where Do the Coordinates Come From? The Embedding Model

You don't place the balloons by hand. An **embedding model** — a neural network trained to capture meaning — takes in text (or an image, or audio) and spits out the vector. Similar inputs produce similar vectors, so "couch" and "sofa" land almost on top of each other even though they share no letters.

Typical dimensions: 384 (MiniLM), 768 (BERT), 1536 (OpenAI `text-embedding-3-small`), 3072 (`text-embedding-3-large`). More dimensions = more nuance, more storage.

---

## Searching by Meaning, Not by Match

This is the whole point:

| | Traditional Database | Vector Database |
|---|---|---|
| **What it stores** | Rows and columns | Embeddings (numbers that encode meaning) |
| **How it searches** | Exact keyword matching | Similarity by meaning |
| **Query style** | "Find the row where `name = 'chair'`" | "Find everything close in meaning to 'seating'" |
| **Partial match** | Fails if the label isn't exact | Works — different words, similar meaning, still match |

Ask a SQL database for "seating" and you get nothing unless a row literally says "seating." Ask a vector database and it returns the chair, the sofa, and the stool — because they're floating right next to each other.

---

## How "Closeness" Is Measured: Cosine Similarity

Think of each embedding as an **arrow**. Cosine similarity measures the **angle** between two arrows, not their length:

| Cosine score | Angle | What it means |
|:---:|:---:|---|
| **1** | 0° | Same direction → nearly identical meaning |
| **0** | 90° | Completely unrelated |
| **−1** | 180° | Opposite meaning |

When you search "seating," the database scores your query arrow against the balloons and returns the ones with cosine closest to **1**. (Dot product and Euclidean distance are the other common metrics — but cosine is the one to understand first.)

---

## How It Stays Fast With Millions of Vectors: ANN

Comparing your query against every single vector would crawl at scale. Vector databases use **Approximate Nearest Neighbor (ANN)** search — instead of checking everything, the algorithm zooms straight into the right neighborhood and returns the closest matches. It trades a sliver of accuracy for a 100–1000× speedup.

It's like a map app showing nearby coffee shops instantly, without inspecting every building in the city. The common algorithms:

- **HNSW** — a multi-layer graph you traverse quickly. The default in most databases.
- **IVF** — partitions vectors into clusters, searches only the relevant ones.
- **Quantization (PQ/SQ/BQ)** — compresses vectors to cut memory 4–32× with minimal recall loss.

---

## The Landscape: Which Vector Database Should You Use?

The space exploded — vector DB adoption grew roughly **377% year-over-year** into 2026, driven almost entirely by RAG. There are 40+ options, but they sort into four buckets:

### 1. Purpose-built vector databases
Engineered from scratch for vectors.
- **Pinecone** — fully managed, serverless, zero-ops. Fastest path to production.
- **Milvus** — open-source, scales to billions, GPU indexing. The self-hosted scale king.
- **Qdrant** — open-source, Rust, excellent filtering, light on resources. Best price/performance.
- **Weaviate** — open-source, multimodal, built-in hybrid (keyword + vector) search.
- **Chroma** — lightweight, embedded, the LLM-prototyping favorite.

### 2. Add vectors to a database you already run
- **pgvector** — vector search *inside* PostgreSQL. Already on Postgres? Start here.
- **Redis** — in-memory vectors for low-latency + caching.
- **Elasticsearch / OpenSearch** — full-text + vector hybrid in a single query.
- **MongoDB Atlas, Cassandra, Neo4j** — document / wide-column / graph stores with vector add-ons.

### 3. Cloud-native managed services
- **Azure AI Search** — enterprise search, wired into Azure OpenAI.
- **AWS** — Amazon OpenSearch Serverless, or Aurora + pgvector.
- **GCP** — Vertex AI Vector Search (ScaNN-based), or AlloyDB AI.
- **Databricks Vector Search** — lakehouse-native, auto-syncs from Delta tables.

### 4. Embedded / lightweight (no server)
- **LanceDB, Chroma (embedded), FAISS, sqlite-vss** — run in-process for edge devices, notebooks, and prototypes.

### When to use which

| Your situation | Reach for |
|---|---|
| Prototyping / local LLM app | **Chroma** or **LanceDB** |
| Want managed, zero-ops, fast to prod | **Pinecone** (or Qdrant Cloud) |
| Self-hosting billions of vectors | **Milvus** |
| High performance + heavy filtering, lean ops | **Qdrant** |
| Already on PostgreSQL | **pgvector** |
| Need hybrid keyword + vector search | **Weaviate**, **Vespa**, or **Elasticsearch/OpenSearch** |
| Multimodal (text + image) | **Weaviate** or **Marqo** |
| All-in on one cloud | **Azure AI Search** / **OpenSearch** / **Vertex AI** |

**The stance: don't reach for a dedicated vector DB on day one.** Start with **pgvector** if you're already on Postgres, or **Chroma** if you're prototyping. Graduate to Pinecone, Qdrant, or Milvus when scale, latency, or ops genuinely force the move — not before. A new piece of infrastructure you don't yet need is a cost, not a feature.

---

## Why This Powers Modern AI: RAG

This is the engine behind **RAG (Retrieval-Augmented Generation)**. Before an LLM answers, it embeds your question, fetches the nearest balloons — the relevant facts — from the vector database, and answers *from them*. That's how chatbots ground their answers instead of hallucinating. The same trick drives Netflix/Spotify recommendations and semantic search that understands intent, not keywords.

> Going deeper on RAG? See [RAG Chunking Strategy](../rag-chunking-strategy/) — a vector DB is only as good as the chunks you feed it.

---

## TL;DR

- A vector database stores data as **embeddings** — coordinates that encode *meaning* — so you search by concept, not exact label.
- An **embedding model** (a neural net) produces the vectors; **cosine similarity** (1 = identical, 0 = unrelated, −1 = opposite) scores closeness; **ANN** keeps it fast at scale.
- Four buckets: **purpose-built** (Pinecone/Milvus/Qdrant/Weaviate/Chroma), **DB extensions** (pgvector/Redis/Elastic), **cloud-native** (Azure AI Search/Vertex/OpenSearch), **embedded** (LanceDB/FAISS).
- Default to **pgvector** (on Postgres) or **Chroma** (prototyping); scale up to Pinecone/Qdrant/Milvus only when you must.

---

## Resources

### YouTube
- [Vector databases are so hot right now. WTF are they? — Fireship](https://www.youtube.com/watch?v=klTvEwg3oJ4)
- [Vector Databases simply explained! (Embeddings & Indexes)](https://www.youtube.com/watch?v=dN0lsF2cvm4)
- [What is a Vector Database? Powering Semantic Search & AI Applications](https://www.youtube.com/watch?v=gl1r1XV0SLw)

### Comparison & benchmarks
- [Superlinked VDB Comparison](https://www.superlinked.com/vector-db-comparison) — 40+ vendors, regularly updated
- [ANN Benchmarks](https://ann-benchmarks.com/) — algorithm-level performance
- [Qdrant Benchmarks](https://qdrant.tech/benchmarks/) — head-to-head comparisons
