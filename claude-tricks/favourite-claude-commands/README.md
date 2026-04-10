# Favourite Claude Code Commands & Tricks

---

## Getting Started

### 1. Always launch from the project root

```bash
cd your-project
claude
```

Claude zips up context from the root directory on launch. Starting from the right place ensures it reads your rule files and understands the project structure from the start.

---

### 2. Generate your initial CLAUDE.md

```bash
/init
```

Claude scans your codebase, understands the architecture, and generates a `CLAUDE.md` rules file automatically. This is essential for new projects — it gives Claude the baseline context it needs to help you effectively.

---

## Essential Slash Commands

### 3. Clear context when switching tasks

```bash
/clear
```

Wipes the current context window so you can start fresh. Use this when you finish a task and don't want old context bleeding into your next feature.

---

### 4. Audit your context usage

```bash
/context
```

Shows a visual breakdown of what's eating your context window — MCPs, files, conversation history. Use it to spot bloat. If your token bill is climbing or Claude feels "dumber", this is where you diagnose it.

---

### 5. Compress long sessions

```bash
/compact
```

Summarizes your current conversation into a condensed version. Claude auto-compacts during long sessions, but you can trigger it manually to save context before it gets too bloated.

---

### 6. Switch models on the fly

```bash
/model
```

Lets you swap between Opus, Sonnet, etc. mid-session. Use Opus when you can afford it — it's the most capable. Drop to Sonnet for cost-sensitive or simpler tasks.

---

### 7. Recover a lost session

```bash
/resume
```

Accidentally killed a Claude instance? This lets you restore the previous conversation and context so you don't lose all the work you put into building that session.

---

### 8. Check installed MCPs

```bash
/mcp
```

Lists all active Model Context Protocol servers. MCPs are powerful but known to blow up your context window. Audit them regularly and only keep what's needed for the current project.

---

### 9. Browse the web from Claude

```bash
/chrome
```

Opens a browser that Claude can control — navigate sites, fill forms, scrape data. Useful when you don't have API access but can reach something through the web.

---

### 10. See all available commands

```bash
/help
```

The full cheat sheet. Lists every slash command, keyboard shortcut, and feature available. Teach a man to fish.

---

## Keyboard Shortcuts

### 11. Toggle between Plan and Edit mode

```
Shift + Tab
```

Switches between **plan mode** (Claude thinks and outlines) and **edit mode** (Claude writes code). Always start in plan mode for new features — verify the approach before executing.

---

### 12. Interrupt Claude mid-response

```
Escape
```

If Claude is going off-track, hit Escape to stop it. Don't be afraid to interrupt — you can press Up to retry or just type a correction. Claude handles multi-prompt queues gracefully.

---

### 13. Clear the input / Rewind

```
Escape, Escape  (double tap)
```

On a filled input: clears everything you typed. On an empty input: opens the rewind menu to restore a previous conversation checkpoint.

---

## Workflow Tips

### 14. Skip all permission prompts (use with caution)

```bash
claude --dangerously-skip-permissions
```

YOLO mode. Claude stops asking for approval on every action. Only use this in throwaway environments. Pair it with `/permissions` to still block truly dangerous operations like `rm -rf`.

---

### 15. Save a workflow as a reusable skill

```
"Save what we just did into a new skill called fetch-hackernews"
```

Skills are recurring workflows saved as `.md` files. Do a task once, then tell Claude to remember it. Next time you can trigger it by name or via a slash command like `/fetch-hackernews`.

---

### 16. Let Claude manage your rules

```
"Update the CLAUDE.md so we never make that mistake again"
```

Don't manually edit `CLAUDE.md`. When Claude does something wrong, fix it and then ask Claude to update its own rules. Think of it like a self-improving lint file.

---

### 17. Run multiple Claude instances in parallel

```bash
# Terminal 1
claude

# Terminal 2 (Cmd+D in iTerm)
claude
```

The real power move. Run multiple sessions side-by-side — one planning, one coding, one researching. Juggle between them like tabs. Use `git worktrees` if multiple instances need to edit the same repo.

---

### 18. Talk to Claude with your voice

```bash
/voice
```

Enables push-to-talk voice dictation — hold `Space` to speak and your words get transcribed directly into the prompt. Great for when you're juggling multiple instances and want to just talk through your intent instead of typing. Requires a Claude.ai account.

---

### 19. Draft and review plans in the browser with ultraplan

```bash
/ultraplan fix the authentication flow and add rate limiting
```

Takes planning to the next level. Claude drafts a detailed plan in a dedicated ultraplan session, then opens it in your browser where you can review and edit it visually. Once you're happy, you can either execute it remotely (on Claude Code on the web) or send it back to your local terminal for execution. Perfect for complex multi-step features where you want a birds-eye view of the plan before committing to it.

---

## Key Principles

| Principle | Why it matters |
|---|---|
| **Context is king** | Give Claude what it needs and nothing more. Bloated context = worse output. |
| **Start in plan mode** | Verify the approach before generating code. Cheaper to fix a plan than rewrite code. |
| **Fresh > bloated** | Clear context between tasks. Don't let old conversations pollute new work. |
| **Validation loops matter** | Put build/test commands in CLAUDE.md so Claude can self-correct without your help. |
| **Keep CLAUDE.md ~300 lines** | Too large = more tokens + weaker instruction following. Prioritize top-to-bottom. |
| **Be selective with MCPs** | Each MCP eats context. Only install what's needed for the current project. |
| **Use sub-agents for atomic tasks** | Protect your main context window. Don't use sub-agents for tasks that need shared context. |
