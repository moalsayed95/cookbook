# Context Engineering

## Resources

### YouTube Videos
- [Effective Context Engineering for AI Agents (why agents still fail in practice)](https://www.youtube.com/watch?v=nkJXADeI62c)

### Articles
- [Effective Context Engineering for AI Agents — Anthropic Engineering](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)

### Docs
- [The Context Window — Claude Code Docs](https://code.claude.com/docs/en/how-claude-code-works#the-context-window)

---

## What is Context Engineering?

Context engineering is the set of strategies for curating and maintaining the optimal set of information fed to an LLM at inference time. Think of it as the evolution of prompt engineering — but instead of crafting a single perfect prompt, you're managing everything the model sees across an entire conversation or agent session.

The goal is simple: find the **smallest set of high-signal tokens** that maximizes the chance of getting the output you want. Context is a finite resource — the more noise you stuff in, the worse the model performs.

## Why Does It Matter?

LLMs don't fail because they're not smart enough. They fail because they're given the wrong context — too much irrelevant information, missing details, or stale data that buries the signal under noise.

This is especially true for AI agents. An agent that runs for 50 turns accumulates massive context. If you don't manage it, the model starts forgetting instructions, misusing tools, and making worse decisions with every step.

Context engineering is the difference between an agent that works in a demo and one that works in production.

## Core Techniques

### System Prompts

Aim for the right altitude — specific enough to guide behavior, flexible enough to handle edge cases. Avoid both brittle hardcoding ("always respond in exactly 3 bullet points") and vague instructions ("be helpful").

### Tool Design

Every tool the model can call takes up context. Design tools that are minimal, have clear purposes, and don't overlap. Bad tool design wastes context through misuse and ambiguity.

### Examples Over Rules

Instead of writing exhaustive edge-case rules, give the model a few diverse, canonical examples. LLMs learn from examples far more effectively than from instructions.

### Just-in-Time Retrieval

Don't pre-load everything into context. Instead, give the agent lightweight references and let it fetch what it needs on demand — the same way you'd Google something instead of memorizing an entire textbook.

### Long-Horizon Strategies

When context fills up over long sessions, you need strategies to keep things working:

| Strategy | How it works |
|----------|-------------|
| **Compaction** | Summarize older conversation history to free up space while keeping continuity |
| **Structured Note-Taking** | The agent writes key findings to external memory instead of relying on context alone |
| **Sub-Agent Architectures** | Delegate focused tasks to specialized agents that return condensed summaries |

## The Context Window

The context window is the total amount of information the model can see at once — your conversation history, file contents, command outputs, system instructions, and tool definitions all compete for the same space.

As you work, context fills up. When it does, older information gets compacted or dropped. Instructions from early in the conversation can get lost entirely. This is why persistent instructions belong in places like `CLAUDE.md` files, not in conversation history.

Key things that consume context:
- **Conversation history** — every message, tool call, and result
- **File contents** — anything the model reads
- **System prompts** — instructions loaded at session start
- **Tool definitions** — every tool the model has access to
- **Retrieved documents** — anything pulled in via RAG or search

The more you understand what's eating your context, the better you can engineer it.

## TL;DR

Context engineering is about feeding the model the right information at the right time — no more, no less. It's the reason some AI agents work reliably and others fall apart after a few turns. Master the context, and you master the output.
