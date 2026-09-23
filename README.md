# VoidStack

> Breaking abstractions. Understanding systems.

A personal engineering portfolio and blog built with [Astro](https://astro.build) — designed to explore cloud infrastructure, backend systems, and software architecture through practical examples and deep technical writing.

## 🚀 Features

- **Fast & Minimal** — Built with Astro for optimal performance
- **Dark/Light Theme** — Toggle between themes with persistent storage
- **Article System** — Technical articles with categorization and publishing dates
- **Project Showcase** — Display of selected projects and work
- **Responsive Design** — Mobile-first, works across all screen sizes
- **SEO Optimized** — Open Graph meta tags, canonical URLs, and semantic HTML

## 📁 Project Structure

```
├── src/
│   ├── components/        # Reusable Astro components
│   ├── content/           # Markdown articles and metadata
│   ├── layouts/           # Page layouts with SEO support
│   ├── pages/             # Routes (index, articles, 404)
│   └── styles/            # Global CSS with theme system
├── public/                # Static assets
├── .env.example           # Environment variables template
├── astro.config.mjs       # Astro configuration
└── package.json           # Dependencies and scripts
```

## 🛠️ Getting Started

### Prerequisites

- Node.js ≥ 22.12.0
- npm or your preferred package manager

### Installation

1. Clone the repository
```bash
git clone <repository-url>
cd voidstack
```

2. Install dependencies
```bash
npm install
```

3. Set up environment variables
```bash
cp .env.example .env
# Edit .env with your contact email and GitHub URL
```

4. Start the development server
```bash
npm run dev
```

The site will be available at `http://localhost:4321`

## 📝 Commands

| Command | Action |
| --- | --- |
| `npm run dev` | Start local dev server |
| `npm run build` | Build production site to `./dist/` |
| `npm run preview` | Preview production build locally |
| `npm run astro` | Run Astro CLI commands |

## ✍️ Writing Articles

Add new articles as Markdown files in `src/content/articles/` with YAML frontmatter:

```markdown
---
title: 'Article Title'
description: 'Brief description'
category: 'CATEGORY'
publishedDate: '2024-01-15'
featured: false
---

# Your article content here...
```

**Required fields:**
- `title` (string) — Article title
- `description` (string) — Short description for preview
- `category` (string) — Content category (e.g., CLOUD, BACKEND, AI)
- `publishedDate` (date) — Publication date in `YYYY-MM-DD` format

**Optional fields:**
- `featured` (boolean) — Mark as featured article (default: false)

## 🎨 Customization

### Environment Variables

Edit `.env` to customize:
- `PUBLIC_CONTACT_EMAIL` — Email for contact section
- `PUBLIC_GITHUB_URL` — GitHub profile link
- `PUBLIC_SITE_URL` — Site URL for SEO (default: http://localhost:4321)
- `PUBLIC_SITE_TITLE` — Site title

### Theme

The site uses CSS custom properties for theming. Edit `src/styles/global.css` to customize colors:
- Dark theme (default) — `:root` variables
- Light theme — `:global(body.light-theme)` overrides

## 📚 Learn More

- [Astro Documentation](https://docs.astro.build)
- [Markdown with Astro](https://docs.astro.build/en/guides/content-collections/)
- [Astro Components](https://docs.astro.build/en/basics/astro-components/)

## 📄 License

This project is open source and available under the MIT License.
