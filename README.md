# VoidStack

A simple personal engineering blog built with [Astro](https://astro.build).

> Breaking abstractions. Understanding systems.

## Features

- **Fast** — Built with Astro for speed
- **Dark/Light Mode** — Toggle between themes
- **Articles** — Technical writing on engineering topics
- **Responsive** — Works on all devices

## Quick Start

### 1. Install

```bash
git clone https://github.com/vinayak-h/voidstack.git
cd voidstack
npm install
```

### 2. Run

```bash
npm run dev
```

Open [http://localhost:4321](http://localhost:4321) in your browser.

### 3. Build

```bash
npm run build
```

## Write an Article

Create a new Markdown file in `src/content/articles/`:

```markdown
---
title: "Your Article Title"
description: "A short description"
category: "BACKEND"
publishedDate: "2026-09-24"
tags:
  - tag1
  - tag2
---

# Your content here

Write your article in Markdown.
```

**Required fields:**
- `title` — Article title
- `description` — Short summary
- `category` — Topic (e.g., BACKEND, CLOUD, AI)
- `publishedDate` — Date in YYYY-MM-DD format

**Optional:**
- `tags` — List of tags
- `featured` — Mark as featured (true/false)

## Commands

```bash
npm run dev       # Start dev server
npm run build     # Build for production
npm run preview   # Preview production build
```

## Deployed On

[Vercel](https://vercel.com) — Auto-deploys on push to main.

## License

Open source and available on [GitHub](https://github.com/vinayak-h/voidstack).
