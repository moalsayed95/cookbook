# Project Scaffolding CLIs — Stop Building Boilerplate by Hand

You've done it: a fresh folder, then 30 minutes wiring up TypeScript, the router, the build config, the folder structure — before writing a single line that does anything. Worse, you've watched an AI agent burn thousands of tokens *generating* that same boilerplate file by file. Both are wasted effort. Every framework ships an official CLI that scaffolds a correct, up-to-date project in one command. Here are the ones worth committing to muscle memory.

## 1. React (Vite)

```bash
npm create vite@latest my-app -- --template react-ts
```

Spins up a React + TypeScript project on **Vite** — instant dev server, hot reload, optimized builds. The `-- --template react-ts` picks the TypeScript React preset (swap for `vue-ts`, `svelte-ts`, etc.). This is the modern default for a React SPA now that Create React App is deprecated.

## 2. Next.js

```bash
npx create-next-app@latest
```

Scaffolds a full **Next.js** app and interactively sets up routing (App Router), TypeScript, ESLint, and Tailwind. You get a production-grade React framework — SSR, file-based routing, API routes — configured correctly from the first commit.

## 3. NestJS (Node backend)

```bash
npx @nestjs/cli new my-backend
```

Generates an entire **enterprise-structured Node backend**: modules, controllers, services, dependency injection, and a test setup, all wired together. Instead of inventing your own folder convention, you start on the one the whole Nest ecosystem already agrees on.

## 4. Django (Python backend)

```bash
pip install django
django-admin startproject my_project
```

Lays down a **Django** project — settings, URL routing, WSGI/ASGI entrypoints, and the `manage.py` command center. From here `python manage.py startapp <name>` scaffolds each app inside it. Batteries included, zero boilerplate written by you.

## More worth pinning

| Stack | Command |
|---|---|
| Vue | `npm create vue@latest` |
| Astro | `npm create astro@latest` |
| React Native | `npx create-expo-app@latest` |
| SvelteKit | `npx sv create my-app` |
| Python (generic) | `uv init my_project` |

## The real power move: put these in your CLAUDE.md

Drop your go-to scaffolding commands into your `CLAUDE.md` (or `.cursorrules`, or any agent's rules file):

```markdown
## Scaffolding
- New React app  -> npm create vite@latest <name> -- --template react-ts
- New Next.js    -> npx create-next-app@latest
- New Nest API   -> npx @nestjs/cli new <name>
- New Django     -> django-admin startproject <name>
```

Now when you say "spin up a new React frontend," the agent runs **one CLI command** instead of hand-authoring 20 boilerplate files. It's faster, it's always current with the framework's latest defaults, and you don't pay tokens for work a maintained tool does for free.

---

## TL;DR

- Never hand-write project boilerplate — every framework has an official scaffolder that does it correctly and current.
- Memorize four: `vite` (React), `create-next-app` (Next), `@nestjs/cli` (Node), `django-admin startproject` (Python).
- Put them in your `CLAUDE.md` so your AI scaffolds via the CLI instead of burning tokens regenerating boilerplate by hand.

---

## Resources

### Docs
- [Vite — Getting Started](https://vite.dev/guide/)
- [create-next-app — Next.js](https://nextjs.org/docs/app/api-reference/cli/create-next-app)
- [NestJS CLI](https://docs.nestjs.com/cli/overview)
- [django-admin startproject](https://docs.djangoproject.com/en/stable/ref/django-admin/#startproject)
