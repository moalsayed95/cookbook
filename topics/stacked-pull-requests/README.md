# GitHub Stacked PRs — Stop Shipping Monster Pull Requests

## The Problem

> "Can you review my PR?"

You open it. **47 files changed. 2,300 lines.** It touches the database schema, the API layer, and the frontend. You close the tab and pretend you didn't see it.

This is every team's bottleneck. The PR is too big to review properly, but splitting it manually means rebase hell — because each layer depends on the one below it. So you ship the monster PR, the reviewer rubber-stamps it, and bugs sneak through.

GitHub's new **Stacked PRs** feature kills this problem. One CLI extension. Your giant PR becomes a chain of small, focused reviews that merge together in a single click.

---

## The Apartment Building Analogy

Think of a large feature like building a 3-story apartment building.

Without stacked PRs, you're asking the city inspector to approve the entire building in one visit — foundation, plumbing, electrical, walls, roof, everything at once. The inspector is overwhelmed, misses the cracked pipe on floor 2, and signs off anyway.

With stacked PRs, you build **one floor at a time**. The inspector reviews just the foundation. Approves it. Then just the plumbing. Approves it. Then the electrical. Each review is small, focused, and actually catches problems.

| Without Stacked PRs | With Stacked PRs |
|---|---|
| One giant PR with 47 files | 3 small PRs with ~15 files each |
| Reviewer skims, rubber-stamps | Reviewer actually reads every line |
| One person reviews everything | Different specialists review each layer |
| Bug in the database layer? Good luck finding it | Bug is isolated to a single, focused PR |
| Takes days to get approved | Layers reviewed in parallel |

---

## How It Works

A stack is an ordered chain of branches. Each branch builds on the one below it, and each gets its own PR. The bottom targets `main`, and every layer above targets the layer below.

```
frontend      → PR #3 (base: api-endpoints)    ← top
api-endpoints → PR #2 (base: db-schema)
db-schema     → PR #1 (base: main)             ← bottom
─────────────
main (trunk)
```

Each PR shows **only the diff for its layer** — not the accumulated diff of everything below it. The reviewer for PR #3 sees only frontend changes, not the database migration that happened two layers down.

```mermaid
flowchart LR
    M["main"] --> DB["db-schema\nPR #1"]
    DB --> API["api-endpoints\nPR #2"]
    API --> FE["frontend\nPR #3"]
    
    style M fill:#6c757d,color:#fff
    style DB fill:#2d6a4f,color:#fff
    style API fill:#e6a23c,color:#fff
    style FE fill:#4a90d9,color:#fff
```

---

## The Commands You Actually Need

### Install

```bash
gh extension install github/gh-stack
```

### Start a stack

```bash
gh stack init
```

Creates a new stack and checks out the first branch. This is your foundation layer.

### Add the next layer

```bash
# Make commits on the current branch, then:
gh stack add api-endpoints
```

Creates a new branch on top of the current one and checks it out. You can also stage, commit, and create a branch in one shot:

```bash
gh stack add -Am "Add API routes"
```

### Push everything and create PRs

```bash
gh stack submit
```

This pushes all branches and opens a PR for each layer. An interactive editor lets you set titles and descriptions for every PR before submitting. GitHub links them together as a stack — reviewers see a stack map at the top of each PR showing where this layer fits.

### View your stack

```bash
gh stack view
```

Shows all branches, their ordering, PR links, and the most recent commit.

### Rebase the stack

```bash
gh stack rebase
```

Fetches latest from `main` and cascading-rebases every branch in the stack. If `main` moved forward, every layer gets updated. If there's a conflict, it pauses and lets you resolve it, then continue with `--continue`.

### Merge everything

```bash
gh stack merge
```

Merges all ready PRs in the stack in a single, all-or-nothing operation. If any PR can't be merged, none are. Your branch protections and required checks still apply — stacked PRs don't bypass anything.

---

## What Happens When a Layer Gets Merged?

This is where the magic is. Say PR #1 (database schema) gets approved and merged into `main` first.

**Without stacked PRs:**
You manually rebase the API branch onto `main`, fix conflicts, push. Then rebase the frontend branch onto the new API branch, fix conflicts, push. Repeat for every layer. Miss one and your PRs show phantom diffs from the already-merged changes.

**With stacked PRs:**
GitHub automatically retargets the remaining PRs. PR #2 now targets `main` instead of the merged `db-schema` branch. The diff stays clean. Run `gh stack sync` to update your local branches:

```bash
gh stack sync
```

This fetches, rebases, pushes, and syncs PR state — all in one command. It even prompts you to prune local branches for merged PRs.

---

## The Full Workflow

```bash
# 1. Start the stack
gh stack init

# 2. Write the database layer
#    ... make commits ...

# 3. Add the API layer on top
gh stack add api-endpoints
#    ... make commits ...

# 4. Add the frontend layer on top
gh stack add frontend-ui
#    ... make commits ...

# 5. Push everything and create PRs
gh stack submit

# 6. Reviewer requests changes on layer 1?
gh stack bottom          # jump to the bottom branch
#    ... fix the issue, commit ...
gh stack rebase          # cascade the fix upward
gh stack push            # push updated branches

# 7. Layer 1 merged? Sync the stack
gh stack sync

# 8. Everything approved? Land it all
gh stack merge
```

---

## When to Use Stacked PRs

### ✅ Perfect for

| Scenario | Why |
|---|---|
| Features with dependent layers (DB → API → UI) | Each layer needs the one below it |
| Refactors that touch many files | Break into logical steps: rename, move, restructure |
| Large features that block review for days | Smaller PRs get reviewed faster |
| Teams with different specialists | Backend reviewer checks layer 1, frontend reviewer checks layer 3 — in parallel |

### ❌ Skip it for

| Scenario | Why |
|---|---|
| Small PRs (< 200 lines) | Stacking adds overhead you don't need |
| Fully independent features | Use regular branches — there's no dependency chain |
| Solo projects with no reviewers | The value is in parallel reviews |

---

## TL;DR

Stop shipping 2,000-line PRs nobody actually reviews. Install `gh extension install github/gh-stack`, break your feature into layers with `gh stack add`, and let your team review each layer in parallel. When a lower layer merges, GitHub rebases the rest automatically. When everything's approved, `gh stack merge` lands the entire chain at once. Your existing branch protections still apply. Zero rebase hell.

---

## Resources

### Docs
- [gh-stack CLI — GitHub](https://github.com/github/gh-stack)
- [Stacked PRs Public Preview Announcement](https://github.blog/changelog/2026-07-30-stacked-pull-requests-are-now-in-public-preview/)
