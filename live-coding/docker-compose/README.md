# Docker Compose — One Command to Rule Them All

![One person orchestrating multiple containers linked together](compose.jpeg)

You have three services. A frontend. A backend. A database. They all need to run **at the same time**, talk to each other, and start in the right order. How do you avoid opening three terminals and praying nothing crashes?

---

## The Orchestra Analogy

![A conductor leading an orchestra — every musician waits for the downbeat](orchestra.jpeg)

Running microservices manually is like conducting an orchestra where every musician starts whenever they feel like it.

The drummer starts before the pianist even sits down. The vocalist sings before the guitarist plugs in. The audience hears chaos.

**Docker Compose is the conductor.** It reads the score (your `docker-compose.yml`), knows who plays first, and brings everyone in at exactly the right time.

| Orchestra | Docker Compose | Why it matters |
|---|---|---|
| 🎼 **Score** | `docker-compose.yml` | The blueprint — who plays, in what order |
| 🥁 **Drummer (foundation)** | Database (Postgres) | Must be ready before anyone else starts |
| 🎸 **Guitarist (melody)** | Backend (FastAPI) | Needs the database alive to connect |
| 🎤 **Vocalist (delivery)** | Frontend (React/Next.js) | Needs the backend alive to fetch data |
| 🎵 **One downbeat** | `docker-compose up` | One command starts the entire performance |

---

## What We're Building

A microservices chat app with three containers:

```mermaid
graph LR
    U["🧑 User"] --> FE["🎤 Frontend\n:3000"]
    FE --> BE["🎸 Backend\n:8000"]
    BE --> DB["🥁 Postgres\n:5432"]
    
    style FE fill:#e63946,stroke:#c1121f,color:#fff
    style BE fill:#457b9d,stroke:#1d3557,color:#fff
    style DB fill:#2d6a4f,stroke:#1b4332,color:#fff
```

All three containers live on the same **isolated virtual network** — they can talk to each other by name (like bandmates calling each other by name backstage), but nothing outside can reach them unless you explicitly open a port.

---

## The File — Line by Line

Create a `docker-compose.yml` in your project root:

```yaml
services:

  # 🥁 The drummer — must be ready before anyone else plays
  database:
    image: pgvector/pgvector:pg16
    ports:
      - "5432:5432"
    environment:
      POSTGRES_USER: chatuser
      POSTGRES_PASSWORD: chatpass
      POSTGRES_DB: chatdb
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U chatuser -d chatdb"]
      interval: 5s
      timeout: 3s
      retries: 5

  # 🎸 The guitarist — waits for the drummer's beat
  backend:
    build: ./backend
    ports:
      - "8000:8000"
    environment:
      DATABASE_URL: postgresql://chatuser:chatpass@database:5432/chatdb
    depends_on:
      database:
        condition: service_healthy

  # 🎤 The vocalist — waits for the guitarist's riff
  frontend:
    build: ./frontend
    ports:
      - "3000:3000"
    depends_on:
      - backend
```

---

## The Three Key Concepts

### 1. Healthchecks — "Are you actually ready?"

> A container being **running** ≠ **ready to accept connections**.

Postgres can take 2–5 seconds to boot. Without a healthcheck, the backend tries to connect immediately, gets "connection refused", and crashes.

The healthcheck runs `pg_isready` every 5 seconds. Only when it passes does Docker mark the container as `healthy`.

```mermaid
sequenceDiagram
    participant D as 🥁 Database
    participant DC as 🎼 Docker Compose
    participant B as 🎸 Backend

    DC->>D: Start container
    D-->>DC: Running (but still booting...)
    DC->>D: pg_isready?
    D-->>DC: ❌ Not yet
    DC->>D: pg_isready?
    D-->>DC: ❌ Not yet
    DC->>D: pg_isready?
    D-->>DC: ✅ Ready!
    DC->>B: OK — start the backend now
    B->>D: Connect to database
    D-->>B: ✅ Connected
```

### 2. `depends_on` — "Don't start until I say so"

```yaml
depends_on:
  database:
    condition: service_healthy
```

This is the magic line. Without the `condition: service_healthy` part, `depends_on` only waits for the container to **start** — not for the service inside to be **ready**. Always pair `depends_on` with a healthcheck.

### 3. Service Networking — "Everyone's backstage together"

Docker Compose automatically creates a shared network. Each service can reach the others **by name**:

```
# Inside the backend container:
postgresql://chatuser:chatpass@database:5432/chatdb
                                ^^^^^^^^
                                This is the service name — not localhost, not an IP
```

No hardcoded IPs. No `host.docker.internal` hacks. Just the service name from your YAML file.

---

## Run It

```bash
docker-compose up
```

That's it. One command. The database starts, the healthcheck passes, the backend connects, and the frontend goes live.

Want to rebuild after code changes?

```bash
docker-compose up --build
```

Want to tear it all down (containers + network)?

```bash
docker-compose down
```

---

## What Happens Under the Hood

```mermaid
graph TD
    CMD["docker-compose up"] --> NET["1. Creates isolated network"]
    NET --> DB["2. Starts database container"]
    DB --> HC["3. Runs healthcheck every 5s"]
    HC -->|"✅ healthy"| BE["4. Starts backend container"]
    BE --> FE["5. Starts frontend container"]
    FE --> DONE["6. All services running + connected"]
    
    style CMD fill:#e63946,stroke:#c1121f,color:#fff
    style NET fill:#6c757d,stroke:#495057,color:#fff
    style DB fill:#2d6a4f,stroke:#1b4332,color:#fff
    style HC fill:#f4a261,stroke:#e76f51,color:#000
    style BE fill:#457b9d,stroke:#1d3557,color:#fff
    style FE fill:#9b2226,stroke:#660708,color:#fff
    style DONE fill:#1d3557,stroke:#0d1b2a,color:#fff
```

---

## Common Gotchas

| Mistake | What happens | Fix |
|---|---|---|
| `depends_on` without `condition: service_healthy` | Backend starts before DB is ready → crash | Add a healthcheck + use `condition: service_healthy` |
| Hardcoding `localhost` in DB connection | Backend can't find the database | Use the **service name** (`database`) instead |
| Forgetting `--build` after code changes | Old code keeps running | Always use `docker-compose up --build` during dev |
| Not mapping ports | Can't reach services from your browser | Add `ports: - "8000:8000"` |

---

## When to Use Docker Compose

| Situation | Use Compose? |
|---|---|
| Local dev with 2+ services | ✅ Absolutely |
| CI/CD pipeline integration tests | ✅ Spin up, test, tear down |
| Production with 100+ containers | ❌ Use [Kubernetes](../../topics/minikube/) |
| Single container, no dependencies | ❌ Just `docker run` |

---

## Related Topics

- **[CI/CD Pipeline](../../topics/ci-cd-pipeline/)** — Docker Compose fits into the "integration test" stage
- **[Minikube](../../topics/minikube/)** — When Compose isn't enough and you need orchestration at scale
- **[Pre-Deployment Checklist](../../topics/pre-deployment-checklist/)** — Containerization is step one
- **[Build Your First API](../build-first-api/)** — The backend service in this demo is a FastAPI app

---

## TL;DR

Docker Compose is a conductor for your microservices. Define every service in one YAML file, wire them together with healthchecks and `depends_on`, and boot the entire system with `docker-compose up`. Use it for local dev and CI testing. Graduate to Kubernetes when you need production-grade orchestration across multiple machines.
