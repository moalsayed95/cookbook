# GitHub Actions

## Resources

### YouTube Videos
- [GitHub Actions — Complete Beginner's Guide (Nana)](https://www.youtube.com/watch?v=R8_veQiYBjI)

### Docs
- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Workflow Syntax Reference](https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax)
- [Events That Trigger Workflows](https://docs.github.com/en/actions/using-workflows/events-that-trigger-workflows)
- [GitHub Actions Marketplace](https://github.com/marketplace?type=actions)

---

## What is GitHub Actions?

GitHub Actions is a **CI/CD platform** built directly into GitHub that lets you automate your build, test, and deployment pipeline. Instead of relying on external tools, you define workflows as YAML files right inside your repository — and GitHub runs them for you on every push, pull request, release, or any other event you choose.

## Core Concepts

### Workflow

A **workflow** is an automated process defined by a YAML file in `.github/workflows/`. A repo can have multiple workflows — one for CI, one for deployment, one for labeling issues — each triggered independently.

### Event

An **event** is the trigger that starts a workflow. Common events:
- `push` — code pushed to a branch
- `pull_request` — PR opened, updated, or merged
- `schedule` — cron-based timer (e.g. nightly builds)
- `workflow_dispatch` — manual trigger from the GitHub UI
- `release` — a new release is published

### Job

A **job** is a set of steps that run on the same runner. By default, jobs run **in parallel**. Use `needs` to make them sequential.

### Step

A **step** is an individual task inside a job — either a shell command (`run`) or a reusable action (`uses`).

### Action

An **action** is a reusable, pre-built unit of work you can plug into any workflow. Thousands are available on the [GitHub Marketplace](https://github.com/marketplace?type=actions). You can also write your own.

### Runner

A **runner** is the server that executes your workflow. GitHub provides hosted runners (Ubuntu, Windows, macOS) or you can self-host your own.

## Workflow File Structure

```yaml
name: CI                          # workflow name

on:                               # trigger(s)
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:                             # one or more jobs
  build:
    runs-on: ubuntu-latest        # runner

    steps:                        # ordered list of steps
      - uses: actions/checkout@v5 # reusable action
      - name: Install deps
        run: npm install          # shell command
      - name: Run tests
        run: npm test
```

## Common Triggers

| Trigger | When it fires |
|---------|---------------|
| `push` | Code is pushed to a branch or tag |
| `pull_request` | A PR is opened, synchronized, or reopened |
| `schedule` | On a cron schedule (e.g. `cron: '0 0 * * *'`) |
| `workflow_dispatch` | Manually via the Actions tab or API |
| `release` | A release is created or published |

## Useful Built-in Actions

| Action | Purpose |
|--------|---------|
| `actions/checkout@v5` | Clone your repo onto the runner |
| `actions/setup-node@v4` | Install a specific Node.js version |
| `actions/setup-python@v5` | Install a specific Python version |
| `actions/cache@v4` | Cache dependencies between runs |
| `actions/upload-artifact@v4` | Save build artifacts |

## Example: CI Pipeline

```yaml
name: Node.js CI

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest

    strategy:
      matrix:
        node-version: [18, 20, 22]

    steps:
      - uses: actions/checkout@v5
      - uses: actions/setup-node@v4
        with:
          node-version: ${{ matrix.node-version }}
      - run: npm ci
      - run: npm test
```

This runs your tests on **three Node versions in parallel** every time you push or open a PR.

## Example: Deploy on Release

```yaml
name: Deploy

on:
  release:
    types: [published]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v5
      - name: Deploy to production
        run: ./deploy.sh
        env:
          API_KEY: ${{ secrets.DEPLOY_API_KEY }}
```

Secrets are stored in **Settings → Secrets and variables → Actions** and are never exposed in logs.

## Key Features

- **Matrix builds** — test across multiple OS/language versions in parallel
- **Secrets management** — encrypted variables for API keys, tokens, etc.
- **Caching** — speed up workflows by caching dependencies
- **Artifacts** — persist build outputs between jobs or download them later
- **Environments** — define deployment targets with protection rules and approvals
- **Concurrency control** — prevent duplicate runs with concurrency groups
- **Reusable workflows** — call shared workflows across repos with `workflow_call`

## Pricing (Quick Summary)

- **Public repos** — unlimited free minutes
- **Private repos** — free tier includes 2,000 minutes/month (varies by plan), then pay-per-minute


