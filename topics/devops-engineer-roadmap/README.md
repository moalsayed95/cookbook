# DevOps Engineer Roadmap 2027

## Resources

### YouTube Videos

**Linux**
- [Linux for Hackers — FREE Linux Course for Beginners (NetworkChuck playlist)](https://www.youtube.com/watch?v=VbEx7B_PTOE&list=PLIhvC56v63IJIujb5cyE13oLuyORZpdkL)

**Programming**
- [Why Learn Python as a DevOps Engineer — Python for DevOps](https://www.youtube.com/watch?v=6u5NE1GiQDk&t=203s)
- [Go Programming — Golang Course with Bonus Projects (freeCodeCamp)](https://www.youtube.com/watch?v=un6ZyFkqFKo&t=2s)
- [Learn JavaScript — Full Course for Beginners (freeCodeCamp)](https://www.youtube.com/watch?v=PkZNo7MFNFg)

**CI/CD**
- [GitHub Actions Tutorial — Basic Concepts and CI/CD Pipeline with Docker (TechWorld with Nana playlist)](https://www.youtube.com/watch?v=R8_veQiYBjI&list=PLy7NrYWoggjzSIlwxeBbcgfAdYoxCIrM2)

**Containers & Orchestration**
- [Docker Crash Course for Absolute Beginners](https://www.youtube.com/watch?v=pg19Z8LL06w)
- [FREE Kubernetes Full Course — CKA Tutorial + Roadmap (playlist)](https://www.youtube.com/watch?v=6_gMoe7Ik8k&list=PLl4APkPHzsUUOkOv3i62UidrLmSB8DcGC)

**Infrastructure as Code**
- [Terraform Tutorial for Beginners + Labs — Complete Step by Step Guide!](https://www.youtube.com/watch?v=YcJ9IeukJL8&t=17s)
- [Introduction to Infrastructure as Code Using Bicep (Microsoft Learn Live playlist)](https://www.youtube.com/watch?v=MP60ND7Upn4&list=PLlrxD0HtieHjzqIRjPoERUGj49rve3rCM)

**Observability & Monitoring**
- [Grafana for Beginners — What is Observability? (playlist)](https://www.youtube.com/watch?v=TQur9GJHIIQ&list=PLDGkOdUX1Ujo27m6qiTPPCpFHVfyKq9jT)

---

DevOps is about **automation** — but you can't automate what you don't understand. This roadmap walks you through each layer from the ground up, so every step builds on the one before it.

## The Roadmap

### Step 1 — Master Linux

Everything in DevOps runs on Linux. Your servers, your containers, your CI runners — all Linux. If you're not comfortable on the command line, nothing else on this roadmap will click.

What to learn:
- Navigating the file system, permissions, users & groups
- Package management (`apt`, `yum`)
- Bash scripting and shell basics
- Networking fundamentals (`ssh`, `curl`, `netstat`, firewalls)
- Process management and systemd

> Start with NetworkChuck's free Linux for Hackers series linked above.

### Step 2 — Learn a Programming Language

DevOps engineers write automation scripts, build tooling, and glue systems together. You need at least one language.

| Language | Why it fits DevOps |
|----------|-------------------|
| **Python** | Most popular for DevOps — scripting, automation, Ansible, AWS Lambda |
| **Go** | Built for infrastructure tooling — Docker, Kubernetes, Terraform are all written in Go |
| **JavaScript** | Useful if you work with full-stack teams or serverless (Node.js, AWS CDK) |

Pick the one that matches your team or interests. Python is the safest default.

### Step 3 — CI/CD Pipelines

Every time a developer pushes code, it should be automatically tested, built, and prepared for deployment. That's CI/CD (Continuous Integration / Continuous Delivery).

Tools to learn:
- **Git** — version control, branching, merging, pull requests
- **GitHub Actions** — define workflows in YAML, run them on every push
- **GitLab CI** — similar concept, built into GitLab
- **Jenkins** — the veteran, self-hosted, highly customizable

What a basic CI pipeline does:

```
Developer pushes code
        ↓
CI server pulls the code
        ↓
Runs tests automatically
        ↓
Builds a Docker image
        ↓
Pushes image to a registry
        ↓
Ready for deployment
```

> Start with the GitHub Actions playlist by TechWorld with Nana linked above — it covers concepts and hands-on Docker integration.

### Step 4 — Containers & Orchestration

Code runs in containers. Containers run in clusters. This is the modern deployment model.

**Docker** — package your application and all its dependencies into a single, portable container that runs the same everywhere.

**Kubernetes** — when you have dozens (or thousands) of containers, Kubernetes orchestrates them: scheduling, scaling, self-healing, load balancing.

**Microservices** — instead of one giant application, you break it into small independent services that each run in their own container and communicate over the network.

| Concept | What it does |
|---------|-------------|
| **Dockerfile** | Instructions to build a container image |
| **Docker Compose** | Run multi-container apps locally |
| **Kubernetes Pod** | Smallest deployable unit — one or more containers |
| **Deployment** | Manages replica sets and rolling updates |
| **Service** | Exposes pods to the network |
| **Ingress** | Routes external traffic to services |

> Watch the Docker Crash Course first, then move to the Kubernetes CKA full course.

### Step 5 — Infrastructure as Code (IaC)

Clicking through cloud consoles doesn't scale. Infrastructure as Code means you define your servers, networks, databases, and everything else in code that can be versioned, reviewed, and reused.

| Tool | Cloud | Language |
|------|-------|----------|
| **Terraform** | Any cloud (AWS, Azure, GCP) | HCL (HashiCorp Configuration Language) |
| **Bicep** | Azure only | Bicep (simplified ARM templates) |
| **Pulumi** | Any cloud | Python, TypeScript, Go |
| **CloudFormation** | AWS only | JSON / YAML |

**Terraform** is the most widely adopted and cloud-agnostic. If your team is Azure-heavy, **Bicep** is worth learning alongside it.

A simple Terraform example:

```hcl
resource "aws_instance" "web" {
  ami           = "ami-0c55b159cbfafe1f0"
  instance_type = "t3.micro"

  tags = {
    Name = "my-web-server"
  }
}
```

One command (`terraform apply`) and your server exists. Another (`terraform destroy`) and it's gone. Repeatable, reviewable, version-controlled.

### Step 6 — Observability & Monitoring

Systems will break. The question is: do you find out from your monitoring dashboard or from an angry user?

**Observability** is about understanding what's happening inside your systems using three pillars:

| Pillar | What it tells you | Tool |
|--------|------------------|------|
| **Metrics** | Numbers over time (CPU, memory, request count, error rate) | Prometheus |
| **Logs** | Detailed event records from your applications | Loki, ELK Stack |
| **Traces** | The journey of a single request across multiple services | Jaeger, Tempo |

**Grafana** ties it all together — it dashboards your metrics, logs, and traces in one place so you can spot issues before your users do.

> Watch the Grafana for Beginners playlist linked above to get started with Prometheus + Grafana.

## The Full Picture

```
Linux (foundation)
  ↓
Programming (Python / Go / JS)
  ↓
CI/CD (Git → GitHub Actions → Jenkins)
  ↓
Containers (Docker → Kubernetes)
  ↓
Infrastructure as Code (Terraform / Bicep)
  ↓
Observability (Prometheus + Grafana)
```

Each layer depends on the one below it. Don't skip ahead.

## One Last Thing

Watching tutorials is not enough. For every course above, **actually build something**. Spin up a Linux VM. Write a real script. Break your Kubernetes cluster and fix it. Deploy infrastructure with Terraform and tear it down. Set up Grafana dashboards for a real app.

The gap between "I watched the tutorial" and "I can do this" is closed by getting your hands dirty.

## TL;DR

DevOps = automation at every layer. Start with Linux → pick a language (Python is the safest bet) → automate builds with CI/CD → containerize with Docker & Kubernetes → define infrastructure as code with Terraform → monitor everything with Prometheus & Grafana. Learn each layer by building, not just watching.
