# The CI/CD Pipeline That Earns a One-Word Deploy

"Nice. Deploy it."

That sentence sounds casual. It isn't. Saying "deploy it" with a straight face means six things are already true in your pipeline — and if even one of them isn't, "deploy it" is how you spend your Friday night rolling back a fire. This is the checklist that turns deployment from a prayer into a non-event.

The examples are GitHub Actions for a FastAPI backend on Azure, but the six ideas are platform-agnostic. Steal them for GitLab CI, Jenkins, whatever you run.

## 1. Secrets come from a vault — never the YAML

**What it means.** Your pipeline needs a database password, an API key, a Stripe secret. None of them live in the repo. The runner **authenticates to Azure with OIDC** (a short-lived, federated token — no stored password) and pulls the real values from **Key Vault at runtime**.

```yaml
- name: Authenticate to Azure (OIDC — zero long-lived credentials)
  uses: azure/login@v2
  with:
    client-id:       ${{ secrets.AZURE_CLIENT_ID }}
    tenant-id:       ${{ secrets.AZURE_TENANT_ID }}
    subscription-id: ${{ secrets.AZURE_SUBSCRIPTION_ID }}

- name: Pull app secrets from Key Vault at runtime
  run: |
    echo "DB_PASSWORD=$(az keyvault secret show --vault-name sayeddev-prod-kv \
      --name DB-PASSWORD --query value -o tsv)" >> "$GITHUB_ENV"
```

**Why it matters before you push.** A secret committed to git is a secret forever — it lives in the history even after you delete it, and bots scrape public repos for exactly this within minutes. OIDC goes one better than "store a service principal secret in GitHub": there's no long-lived credential to leak in the first place. The `client-id` and `tenant-id` above are *identifiers*, not passwords.

## 2. Dependencies are cached — builds are minutes, not coffee breaks

**What it means.** Re-downloading and reinstalling every package on every run is wasted time. Cache the dependency layer and a 20-minute build collapses to under two. On GitHub Actions it's one line:

```yaml
- uses: actions/setup-python@v5
  with:
    python-version: '3.11'
    cache: 'pip'        # ← that's the whole trick
```

**Why it matters before you scale the team.** This isn't micro-optimization — it's the difference between a feedback loop people *use* and one they route around. When CI takes 20 minutes, developers stop waiting for it and start merging on hope. When it takes 90 seconds, the pipeline becomes a reflex. Slow CI doesn't just cost minutes; it quietly erodes the habit of trusting CI at all.

## 3. `main` is protected — no human pushes to it directly

**What it means.** Branch protection makes the path to production a one-way street: you open a **pull request**, the **tests must pass**, and at least **one other human approves**. No force-pushes, no "quick hotfix straight to main."

A ruleset that actually protects `main` requires:
- ✅ Pull request before merging
- ✅ Status checks (your test job) must pass
- ✅ At least 1 approving review
- ✅ Branch up to date with `main` before merge

**Why it matters before you have teammates.** The moment more than one person can push to `main`, "it works on my machine" becomes everyone's problem. Picture the 5pm-Friday hotfix shoved straight to `main` with no review — it skips the one checkpoint that would've caught the typo, and now it's live. If a human *can* push to `main`, `main` is not protected. A green checkmark and a second pair of eyes is the cheapest insurance in software.

## 4. Every PR is scanned for vulnerable packages — and the scan can block the merge

**What it means.** An automated security scan runs on each pull request and inspects your dependency tree for known CVEs. The key word is **gate**: a finding fails the check, and a failed check (item 3) blocks the merge.

```yaml
- name: Audit dependencies for known CVEs
  run: |
    pip install pip-audit
    pip-audit -r requirements.txt   # non-zero exit fails the PR
```

**Why it matters before you trust your supply chain.** You don't get breached through the package you chose — you get breached through the package *your package* depends on, three levels down, that shipped a backdoor overnight (see the xz incident). A scan that only emails you a warning is just a notification you'll learn to ignore. A scan wired into branch protection is a wall. Make it a wall.

## 5. Schema changes run as migrations — against staging, before traffic moves

**What it means.** Database changes are **versioned migrations** (e.g., Alembic), not someone running ad-hoc SQL against prod. The pipeline applies them to a **staging slot** — a full, warm copy of production — and only then shifts real traffic onto the new version.

**Why it matters before users are on the line.** Schema and code have to move in lockstep. Run a migration that drops a column while the old pods are still serving requests, and every one of those requests starts 500ing until the rollout finishes. Staging-first means the migration and the new code prove they work *together* on a production-shaped environment before a single user is exposed. Migrations also give you a written, reversible history — the opposite of "what did we change last Tuesday?"

## 6. Health checks gate the rollout — and failure rolls back instantly

**What it means.** After deploy, automated **health checks** probe the new version (a `/health` endpoint, readiness/liveness checks). If they pass, traffic swaps over. If they fail, the platform **automatically reverts to the last good version** — no human, no panic.

On Azure App Service this is *swap with preview*: warm up the staging slot, health-check it, swap into production, and on failure swap straight back. The old version never actually left.

**Why it matters before real traffic hits it.** Code that's green in CI can still crash on the first real request — a missing env var, a region that's down, a dependency that times out under load. Without a rollback gate, your users *are* your smoke test, and the time-to-recovery is "however long until someone wakes up." With one, a bad deploy is a 30-second blip that auto-heals. Mean-time-to-recovery beats mean-time-between-failures every time.

---

## TL;DR

Before anyone gets to say "deploy it," the pipeline has to have earned it:

1. **Vault secrets** — OIDC + Key Vault at runtime; nothing sensitive in the YAML or git history.
2. **Dependency caching** — sub-2-minute builds, so CI stays a reflex instead of a tax.
3. **Branch protection** — PRs, passing tests, and an approval; no human pushes `main`.
4. **Security gate** — every PR scanned for CVEs, and the scan *blocks* the merge.
5. **Staging migrations** — versioned schema changes proven on a prod-shaped slot first.
6. **Health-checked rollback** — the rollout watches itself and instantly reverts on failure.

None of these are "nice to have." Each one converts a specific class of 2am page into a non-event — and the one you label "we'll add it later" is statistically the one that breaks first.

---

## Resources

### Related in this cookbook
- [GitHub Actions](../github-actions/) — the fundamentals of the workflow file these snippets live in
- [Pre-Deployment Checklist](../pre-deployment-checklist/) — the manual checks that complement an automated pipeline

### Docs
- [GitHub OIDC with Azure](https://docs.github.com/en/actions/deployment/security-hardening-your-deployments/configuring-openid-connect-in-azure)
- [Caching dependencies — GitHub Actions](https://docs.github.com/en/actions/using-workflows/caching-dependencies-to-speed-up-workflows)
- [About protected branches — GitHub](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches)
- [pip-audit](https://github.com/pypa/pip-audit) · [Dependabot](https://docs.github.com/en/code-security/dependabot)
- [Set up staging environments — Azure App Service slots](https://learn.microsoft.com/azure/app-service/deploy-staging-slots)
