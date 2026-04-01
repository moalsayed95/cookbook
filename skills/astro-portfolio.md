---
name: astro-portfolio
description: Build a polished one-page personal portfolio website using Astro 5, Tailwind CSS v4, and Vercel. Uses the "Terminal Luxe" design system — dark theme, teal/violet accents, staggered animations, and atmospheric background effects. Use this skill whenever the user wants to create a personal website, portfolio, landing page, developer profile page, or one-page site. Also use when they mention Astro with Tailwind, or want a dark-themed modern portfolio. This skill is beginner-friendly and walks through everything from installing Node.js to deploying on Vercel.
---

# Astro Portfolio — Terminal Luxe

Build a production-ready one-page portfolio website with Astro 5, Tailwind CSS v4, and Vercel deployment. The design system is called "Terminal Luxe" — a premium dark aesthetic that blends terminal/developer culture with polished modern design.

This skill is designed for all skill levels, including people who have never written code before. Guide users through every step clearly.

## Tech Stack

| Tool | Role |
|------|------|
| **Astro 5** | Static site framework — outputs plain HTML, no JavaScript shipped to the browser |
| **Tailwind CSS v4** | Styling via utility classes, configured as a Vite plugin (no config file needed) |
| **Google Fonts** | Syne (headings), Outfit (body text), JetBrains Mono (code/terminal style) |
| **Vercel** | Free hosting with automatic deploys when you push code |

## Before You Start — Prerequisites

Before writing any code, walk the user through these setup steps. Ask what they already have installed to skip what's not needed.

### 1. Install Node.js

Node.js is the engine that runs the development tools. Go to https://nodejs.org and download the LTS (Long Term Support) version. Run the installer. To verify it worked, open a terminal and type:

```bash
node --version
```

If you see a version number (like `v22.x.x`), you're good.

### 2. Set up a code editor

Recommend **VS Code** (Visual Studio Code) — it's free and beginner-friendly. After installing it, install these extensions for the best experience:

- **Astro** (by Astro) — syntax highlighting and IntelliSense for `.astro` files
- **Tailwind CSS IntelliSense** (by Tailwind Labs) — autocomplete for Tailwind classes

### 3. Create a GitHub account

If the user doesn't have one, they'll need a free GitHub account at https://github.com to deploy their site on Vercel later.

### 4. Create a Vercel account

Sign up at https://vercel.com using their GitHub account. This links the two together for automatic deployments.

---

## Step-by-Step Build

### Step 1: Scaffold the Astro project

Run this in the terminal:

```bash
npm create astro@latest my-portfolio -- --template minimal
cd my-portfolio
```

When prompted, accept the defaults. This creates a bare-bones Astro project.

### Step 2: Install dependencies

```bash
npm install @astrojs/vercel @tailwindcss/vite tailwindcss
```

These three packages are:
- `@astrojs/vercel` — lets Astro deploy to Vercel
- `tailwindcss` — the CSS framework
- `@tailwindcss/vite` — plugs Tailwind into Astro's build system

### Step 3: Configure Astro

Replace the contents of `astro.config.mjs` with:

```js
// @ts-check
import { defineConfig } from 'astro/config';
import vercel from '@astrojs/vercel';
import tailwindcss from '@tailwindcss/vite';

export default defineConfig({
  output: 'static',
  adapter: vercel(),
  vite: {
    plugins: [tailwindcss()]
  }
});
```

What this does:
- `output: 'static'` — pre-builds all pages as plain HTML (fast, free to host)
- `adapter: vercel()` — tells Astro how to package the site for Vercel
- `tailwindcss()` as a Vite plugin — this is Tailwind v4's approach, no `tailwind.config.js` needed

### Step 4: Create the global stylesheet

Create the file `src/styles/global.css`:

```css
@import "tailwindcss";

@custom-variant dark (&:where(.dark, .dark *));

@theme {
  --font-family-display: "Syne", sans-serif;
  --font-family-body: "Outfit", sans-serif;
  --font-family-mono: "JetBrains Mono", monospace;
  --color-accent: #7dd3c4;

  --animate-fade-up: fade-up 0.7s cubic-bezier(0.16, 1, 0.3, 1) forwards;
  --animate-fade-in: fade-in 0.5s ease-out forwards;
  --animate-glow: glow-pulse 4s ease-in-out infinite;
  --animate-float: float 6s ease-in-out infinite;
  --animate-wave: wave 2.5s ease-in-out infinite;
}

@keyframes fade-up {
  from { opacity: 0; transform: translateY(24px); }
  to { opacity: 1; transform: translateY(0); }
}

@keyframes fade-in {
  from { opacity: 0; }
  to { opacity: 1; }
}

@keyframes glow-pulse {
  0%, 100% { opacity: 0.4; transform: scale(1); }
  50% { opacity: 0.6; transform: scale(1.08); }
}

@keyframes float {
  0%, 100% { transform: translateY(0px); }
  50% { transform: translateY(-12px); }
}

@keyframes wave {
  0%, 100% { transform: rotate(0deg); }
  10%, 30% { transform: rotate(14deg); }
  20% { transform: rotate(-8deg); }
  40% { transform: rotate(-4deg); }
  50% { transform: rotate(10deg); }
}

.stagger-1 { animation-delay: 0.1s; }
.stagger-2 { animation-delay: 0.2s; }
.stagger-3 { animation-delay: 0.35s; }
.stagger-4 { animation-delay: 0.5s; }
.stagger-5 { animation-delay: 0.65s; }
.stagger-6 { animation-delay: 0.8s; }
.stagger-7 { animation-delay: 0.95s; }
```

Key concepts to explain to the user:
- `@import "tailwindcss"` — this single line loads the entire Tailwind framework (v4 style)
- `@custom-variant dark` — tells Tailwind that `dark:` classes activate when `<html>` has the `.dark` class (instead of using the OS setting)
- `@theme` — registers custom design tokens (fonts, colors, animations) that become usable as Tailwind utilities like `font-display`, `text-accent`, `animate-fade-up`
- The `@keyframes` define smooth entrance animations and atmospheric effects
- The `.stagger-*` classes add incremental delays so elements animate in one after another

### Step 5: Create the layout

Create `src/layouts/BaseLayout.astro`:

```astro
---
import '../styles/global.css';

interface Props {
  title: string;
  description: string;
  ogImage?: string;
  ogUrl?: string;
}

const { title, description, ogImage, ogUrl } = Astro.props;
---

<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title}</title>
  <meta name="description" content={description}>

  <!-- Favicon -->
  <link rel="icon" type="image/svg+xml" href="/favicon.svg">

  <!-- Theme Color (browser tab color on mobile) -->
  <meta name="theme-color" content="#ffffff">
  <meta name="theme-color" content="#060606" media="(prefers-color-scheme: dark)">

  <!-- Fonts -->
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Syne:wght@400;500;600;700;800&family=Outfit:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">

  {ogImage && (
    <Fragment>
      <meta property="og:title" content={title}>
      <meta property="og:description" content={description}>
      <meta property="og:type" content="website">
      {ogUrl && <meta property="og:url" content={ogUrl}>}
      <meta property="og:image" content={ogImage}>
      <meta name="twitter:card" content="summary_large_image">
      <meta name="twitter:title" content={title}>
      <meta name="twitter:description" content={description}>
      <meta name="twitter:image" content={ogImage}>
    </Fragment>
  )}

  <!-- Prevent flash of wrong theme: apply dark mode BEFORE the page renders -->
  <script is:inline>
    (function() {
      var saved = localStorage.getItem('theme');
      if (saved === 'dark' || (!saved && window.matchMedia('(prefers-color-scheme: dark)').matches)) {
        document.documentElement.classList.add('dark');
      }
    })();
  </script>
</head>
<body class="bg-white text-gray-900 dark:bg-[#060606] dark:text-white font-body antialiased overflow-x-hidden">

  <!-- Background Atmosphere — decorative glowing orbs and dot grid -->
  <div class="fixed inset-0 pointer-events-none overflow-hidden" aria-hidden="true">
    <div class="absolute -top-32 -right-32 w-[500px] h-[500px] rounded-full bg-accent/[0.07] blur-[128px] animate-glow opacity-0 dark:opacity-100"></div>
    <div class="absolute -bottom-48 -left-48 w-[600px] h-[600px] rounded-full bg-violet-500/[0.06] blur-[128px] animate-glow opacity-0 dark:opacity-100" style="animation-delay: 2s;"></div>
    <div class="absolute inset-0 opacity-[0.04] dark:opacity-[0.025]" style="background-image: radial-gradient(circle, currentColor 1px, transparent 1px); background-size: 32px 32px;"></div>
  </div>

  <slot />

  <!-- Theme Toggle Logic -->
  <script is:inline>
    document.getElementById('theme-toggle').addEventListener('click', function() {
      var isDark = document.documentElement.classList.toggle('dark');
      localStorage.setItem('theme', isDark ? 'dark' : 'light');
    });
  </script>

</body>
</html>
```

Explain these patterns to the user:
- **`<slot />`** — this is where page content gets injected. Think of the layout as a picture frame, and each page is the picture that goes inside it.
- **`is:inline`** — tells Astro to keep this script as-is in the HTML (not bundle it). The theme script MUST be inline so it runs before anything paints, preventing a flash of the wrong theme.
- **`pointer-events-none` + `aria-hidden`** — the background orbs are purely decorative and shouldn't interfere with clicking or screen readers.
- **Open Graph meta tags** — these control how the site looks when shared on social media (the image, title, and description that appear in the link preview).

### Step 6: Create the main page

Create `src/pages/index.astro`:

```astro
---
import BaseLayout from '../layouts/BaseLayout.astro';
---

<BaseLayout
  title="Your Name | Your Title"
  description="A short description of what you do."
>

  <!-- Header -->
  <header class="relative z-10 px-6 md:px-12 py-6 opacity-0 animate-fade-in">
    <div class="max-w-5xl mx-auto flex items-center justify-between">
      <a href="/" class="font-display font-bold text-lg tracking-tight text-gray-900 dark:text-white hover:text-accent transition-colors duration-300">
        your name
      </a>
      <button
        id="theme-toggle"
        type="button"
        class="p-2 rounded-lg text-gray-500 dark:text-neutral-500 hover:text-accent transition-colors duration-300"
        aria-label="Toggle dark mode"
      >
        <!-- Sun icon (visible in dark mode) -->
        <svg class="w-5 h-5 hidden dark:block" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5">
          <path stroke-linecap="round" stroke-linejoin="round" d="M12 3v2.25m6.364.386l-1.591 1.591M21 12h-2.25m-.386 6.364l-1.591-1.591M12 18.75V21m-4.773-4.227l-1.591 1.591M5.25 12H3m4.227-4.773L5.636 5.636M15.75 12a3.75 3.75 0 11-7.5 0 3.75 3.75 0 017.5 0z" />
        </svg>
        <!-- Moon icon (visible in light mode) -->
        <svg class="w-5 h-5 block dark:hidden" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5">
          <path stroke-linecap="round" stroke-linejoin="round" d="M21.752 15.002A9.718 9.718 0 0118 15.75c-5.385 0-9.75-4.365-9.75-9.75 0-1.33.266-2.597.748-3.752A9.753 9.753 0 003 11.25C3 16.635 7.365 21 12.75 21a9.753 9.753 0 009.002-5.998z" />
        </svg>
      </button>
    </div>
  </header>

  <!-- Hero Section -->
  <main class="relative z-10">
    <section class="pt-16 md:pt-24 pb-20 px-6 md:px-12">
      <div class="max-w-5xl mx-auto w-full">
        <div class="grid grid-cols-1 md:grid-cols-2 gap-10 md:gap-16 items-center">

          <!-- Text Content -->
          <div class="order-2 md:order-1 text-center md:text-left">

            <h1 class="font-display font-extrabold text-5xl md:text-6xl lg:text-7xl leading-[1.08] tracking-tight opacity-0 animate-fade-up stagger-1">
              Hey, I'm<br>
              Your Name <span class="inline-block animate-wave origin-[70%_70%]">👋</span>
            </h1>

            <!-- Role Badges -->
            <div class="flex flex-wrap gap-3 mt-7 justify-center md:justify-start opacity-0 animate-fade-up stagger-2">
              <span class="inline-flex items-center gap-2 px-4 py-1.5 rounded-full text-sm font-medium border border-accent/30 dark:border-accent/20 text-accent bg-accent/[0.08] dark:bg-accent/[0.06]">
                <span class="w-1.5 h-1.5 rounded-full bg-accent"></span>
                Your Role
              </span>
              <span class="inline-flex items-center gap-2 px-4 py-1.5 rounded-full text-sm font-medium border border-violet-400/30 dark:border-violet-400/20 text-violet-500 dark:text-violet-400 bg-violet-400/[0.08] dark:bg-violet-400/[0.06]">
                <span class="w-1.5 h-1.5 rounded-full bg-violet-400"></span>
                Another Role
              </span>
            </div>

            <!-- Tagline -->
            <p class="mt-6 text-lg md:text-xl text-gray-500 dark:text-neutral-400 leading-relaxed max-w-lg mx-auto md:mx-0 opacity-0 animate-fade-up stagger-3">
              A short, memorable line about what you do.
            </p>

            <!-- Terminal Line -->
            <div class="mt-4 font-mono text-sm text-gray-400 dark:text-neutral-600 opacity-0 animate-fade-up stagger-4">
              <span class="text-accent">$</span> currently building cool stuff<span class="animate-blink">_</span>
            </div>

            <!-- Social Links -->
            <div class="flex items-center gap-5 mt-10 justify-center md:justify-start opacity-0 animate-fade-up stagger-5">
              <span class="text-[11px] font-mono text-gray-400 dark:text-neutral-600 uppercase tracking-[0.2em]">find me</span>
              <div class="h-px w-6 bg-gray-300 dark:bg-neutral-800"></div>

              <!-- GitHub -->
              <a href="https://github.com/yourhandle" target="_blank" rel="noopener noreferrer" class="text-gray-400 dark:text-neutral-600 hover:text-accent transition-colors duration-300" aria-label="GitHub">
                <svg class="w-[18px] h-[18px]" fill="currentColor" viewBox="0 0 24 24">
                  <path d="M12 .297c-6.63 0-12 5.373-12 12 0 5.303 3.438 9.8 8.205 11.385.6.113.82-.258.82-.577 0-.285-.01-1.04-.015-2.04-3.338.724-4.042-1.61-4.042-1.61C4.422 18.07 3.633 17.7 3.633 17.7c-1.087-.744.084-.729.084-.729 1.205.084 1.838 1.236 1.838 1.236 1.07 1.835 2.809 1.305 3.495.998.108-.776.417-1.305.76-1.605-2.665-.3-5.466-1.332-5.466-5.93 0-1.31.465-2.38 1.235-3.22-.135-.303-.54-1.523.105-3.176 0 0 1.005-.322 3.3 1.23.96-.267 1.98-.399 3-.405 1.02.006 2.04.138 3 .405 2.28-1.552 3.285-1.23 3.285-1.23.645 1.653.24 2.873.12 3.176.765.84 1.23 1.91 1.23 3.22 0 4.61-2.805 5.625-5.475 5.92.42.36.81 1.096.81 2.22 0 1.606-.015 2.896-.015 3.286 0 .315.21.69.825.57C20.565 22.092 24 17.592 24 12.297c0-6.627-5.373-12-12-12"/>
                </svg>
              </a>

              <!-- LinkedIn -->
              <a href="https://linkedin.com/in/yourhandle" target="_blank" rel="noopener noreferrer" class="text-gray-400 dark:text-neutral-600 hover:text-accent transition-colors duration-300" aria-label="LinkedIn">
                <svg class="w-[18px] h-[18px]" fill="currentColor" viewBox="0 0 24 24">
                  <path d="M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433c-1.144 0-2.063-.926-2.063-2.065 0-1.138.92-2.063 2.063-2.063 1.14 0 2.064.925 2.064 2.063 0 1.139-.925 2.065-2.064 2.065zm1.782 13.019H3.555V9h3.564v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 23.227.792 24 1.771 24h20.451C23.2 24 24 23.227 24 22.271V1.729C24 .774 23.2 0 22.222 0h.003z"/>
                </svg>
              </a>

              <!-- X / Twitter -->
              <a href="https://x.com/yourhandle" target="_blank" rel="noopener noreferrer" class="text-gray-400 dark:text-neutral-600 hover:text-accent transition-colors duration-300" aria-label="X">
                <svg class="w-[18px] h-[18px]" fill="currentColor" viewBox="0 0 24 24">
                  <path d="M18.244 2.25h3.308l-7.227 8.26 8.502 11.24H16.17l-5.214-6.817L4.99 21.75H1.68l7.73-8.835L1.254 2.25H8.08l4.713 6.231zm-1.161 17.52h1.833L7.084 4.126H5.117z"/>
                </svg>
              </a>
            </div>

          </div>

          <!-- Profile Image -->
          <div class="order-1 md:order-2 flex justify-center opacity-0 animate-fade-up stagger-2">
            <div class="relative group">
              <!-- Glow effect behind image on hover -->
              <div class="absolute -inset-1 bg-gradient-to-br from-accent/40 to-violet-500/40 rounded-2xl blur-md opacity-0 dark:opacity-50 group-hover:opacity-40 dark:group-hover:opacity-75 transition-opacity duration-700"></div>
              <img
                src="/profile.jpg"
                alt="Your Name"
                class="relative w-36 h-36 md:w-44 md:h-44 lg:w-52 lg:h-52 rounded-2xl object-cover border border-gray-200 dark:border-neutral-800/80"
              />
            </div>
          </div>

        </div>
      </div>
    </section>
  </main>

  <!-- Footer -->
  <footer class="relative z-10 py-8 text-center">
    <p class="text-xs font-mono text-gray-300 dark:text-neutral-800">yourname.dev &mdash; 2025</p>
  </footer>

  <!-- Blinking cursor animation -->
  <style>
    @keyframes blink {
      0%, 50% { opacity: 1; }
      51%, 100% { opacity: 0; }
    }
    .animate-blink {
      animation: blink 1s step-end infinite;
    }
  </style>

</BaseLayout>
```

Tell the user to replace all placeholder text: "Your Name", "Your Role", "Another Role", the tagline, terminal line, social links, and the profile image.

### Step 7: Create the favicon

Create `public/favicon.svg`. This is a simple branded icon — a single letter on a dark rounded square:

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32" fill="none">
  <rect width="32" height="32" rx="8" fill="#060606"/>
  <text x="16" y="23" font-family="Arial, sans-serif" font-size="20" font-weight="bold" text-anchor="middle" fill="#7dd3c4">Y</text>
</svg>
```

The user should change the letter "Y" to their own initial.

### Step 8: Add a profile image

Tell the user to place their profile photo in the `public/` folder as `profile.jpg`. This image appears in the hero section. A square image works best (it gets cropped to a rounded square). Recommend keeping it under 500KB for fast loading.

---

## Customization Guide

After the base site is working, walk the user through personalizing it:

### Changing colors

The two brand colors are defined in `global.css` under `@theme`:
- **Accent** (`--color-accent: #7dd3c4`) — the teal used for highlights, links, and the terminal prompt. Change this to any color that represents them.
- **Violet** — used directly in Tailwind classes like `bg-violet-500`. To change it, search and replace `violet` with another Tailwind color name (e.g., `rose`, `blue`, `amber`).
- **Background** (`#060606`) — the near-black dark mode background, set in the `<body>` class.

### Adding or removing social links

Each social link in `index.astro` follows this pattern:

```html
<a href="https://platform.com/yourhandle" target="_blank" rel="noopener noreferrer"
   class="text-gray-400 dark:text-neutral-600 hover:text-accent transition-colors duration-300"
   aria-label="Platform Name">
  <svg class="w-[18px] h-[18px]" fill="currentColor" viewBox="0 0 24 24">
    <!-- SVG path for the icon -->
  </svg>
</a>
```

To add a platform: copy one of the existing link blocks, swap in the new SVG icon (search "[platform name] SVG icon" online), and update the `href` and `aria-label`. To remove one: delete the entire `<a>...</a>` block.

### Adding or removing role badges

Each badge is a `<span>` element. Copy the pattern and change the text. Use `border-accent` classes for teal badges or `border-violet-400` classes for violet badges. Mix and match.

### Changing fonts

The three fonts are loaded in `BaseLayout.astro` via Google Fonts and registered in `global.css` under `@theme`. To swap a font:
1. Pick a font from https://fonts.google.com
2. Update the Google Fonts `<link>` URL in `BaseLayout.astro`
3. Update the corresponding `--font-family-*` variable in `global.css`

---

## Deploying to Vercel

### First-time setup

1. **Push code to GitHub**: If the user hasn't used Git before, walk them through:
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   ```
   Then create a new repository on GitHub (the "+" button → "New repository"), and follow the instructions to push:
   ```bash
   git remote add origin https://github.com/yourhandle/my-portfolio.git
   git branch -M main
   git push -u origin main
   ```

2. **Connect to Vercel**:
   - Go to https://vercel.com/new
   - Click "Import" next to the GitHub repository
   - Vercel auto-detects Astro — no configuration needed
   - Click "Deploy"

3. **Done**. Vercel gives a live URL immediately (something like `my-portfolio.vercel.app`).

### Custom domain (optional)

If the user has a custom domain:
1. Go to the Vercel project → Settings → Domains
2. Add the domain name
3. Update DNS records at their domain registrar (Vercel shows exactly what to set)

### Automatic deploys

After the initial setup, every time the user pushes code to GitHub, Vercel automatically rebuilds and deploys the site. The workflow becomes:

```bash
git add .
git commit -m "Update portfolio"
git push
```

That's it — the live site updates in about 30 seconds.

---

## Running locally during development

To see the site while working on it:

```bash
npm run dev
```

This starts a local server (usually at `http://localhost:4321`). Changes appear instantly in the browser as the user edits files. Press `Ctrl+C` to stop the server.

---

## File Structure Reference

```
my-portfolio/
├── public/
│   ├── favicon.svg          ← Browser tab icon
│   └── profile.jpg          ← Your profile photo
├── src/
│   ├── layouts/
│   │   └── BaseLayout.astro ← Shared page shell (head, fonts, dark mode, background)
│   ├── pages/
│   │   └── index.astro      ← The portfolio page itself
│   └── styles/
│       └── global.css        ← Tailwind + design tokens + animations
├── astro.config.mjs          ← Astro configuration
└── package.json              ← Project dependencies
```

---

## Design System Reference — Terminal Luxe

| Token | Value | Used for |
|-------|-------|----------|
| Background (dark) | `#060606` | Page background in dark mode |
| Accent | `#7dd3c4` | Links, highlights, terminal prompt, badges |
| Violet | `#a855f7` | Secondary badge, background orb, image glow |
| Font — Display | Syne | Headings, logo, CTA buttons |
| Font — Body | Outfit | Paragraphs, descriptions |
| Font — Mono | JetBrains Mono | Terminal line, footer, labels |

### Animation system

Elements enter the page with staggered `fade-up` animations. Each element starts invisible (`opacity-0`) and has two classes:
- `animate-fade-up` — slides up 24px while fading in
- `stagger-N` — delays the animation by an incremental amount (1 = 0.1s, 2 = 0.2s, etc.)

This creates a cascading "reveal" effect where the page content flows in top to bottom.

### Dark mode system

- Theme stored in `localStorage` under key `"theme"` (values: `"dark"` or `"light"`)
- On page load, an inline script in `<head>` applies `.dark` to `<html>` before paint
- The toggle button switches the class and saves the preference
- All dark-mode styles use Tailwind's `dark:` prefix (e.g., `dark:bg-[#060606]`)
