# 🚀 Astro + MDX blog scaffold (dark-first, minimalist)

> Drop-in starter to migrate your current single-page site to Astro with an MDX-powered blog. Includes Tailwind, content collections, code highlighting, RSS, and a clean dark-first theme.

---

## 0) Prereqs & init
```bash
# Node 18+ recommended
corepack enable || true

# Create project
mkdir autumn-site && cd autumn-site
npm init -y
npm install astro @astrojs/mdx @astrojs/tailwind @astrojs/rss zod
npm install -D tailwindcss postcss autoprefixer

# Optional icons
npm install lucide-static # simple SVGs
```

---

## 1) File tree
```
autumn-site/
  astro.config.mjs
  package.json
  tailwind.config.cjs
  postcss.config.cjs
  tsconfig.json
  src/
    content/
      config.ts
      blog/
        hello-world.mdx
    components/
      Header.astro
      Footer.astro
      PostCard.astro
      Prose.astro
    layouts/
      Base.astro
      PostLayout.astro
    pages/
      index.astro
      blog/
        index.astro
        [slug].astro
      rss.xml.ts
    styles/
      globals.css
```

---

## 2) Config files

### `package.json`
```json
{
  "name": "autumn-site",
  "private": true,
  "type": "module",
  "scripts": {
    "dev": "astro dev",
    "build": "astro build",
    "preview": "astro preview"
  },
  "dependencies": {
    "@astrojs/mdx": "^3.1.0",
    "@astrojs/rss": "^4.0.0",
    "@astrojs/tailwind": "^5.1.0",
    "astro": "^4.12.0",
    "zod": "^3.23.8"
  },
  "devDependencies": {
    "autoprefixer": "^10.4.19",
    "postcss": "^8.4.38",
    "tailwindcss": "^3.4.7"
  }
}
```

### `astro.config.mjs`
```js
import { defineConfig } from 'astro/config'
import mdx from '@astrojs/mdx'
import tailwind from '@astrojs/tailwind'

export default defineConfig({
  integrations: [mdx(), tailwind({ applyBaseStyles: false })],
  markdown: {
    syntaxHighlight: 'shiki',
    shikiConfig: {
      theme: 'github-dark-dimmed'
    }
  },
  site: 'https://autumnnippert.com'
})
```

### `tailwind.config.cjs`
```js
/** @type {import('tailwindcss').Config} */
module.exports = {
  darkMode: 'class',
  content: [
    './src/**/*.{astro,md,mdx,js,ts,tsx}'
  ],
  theme: {
    extend: {
      colors: {
        bg: {
          DEFAULT: '#0B0F14',
          soft: '#0F1520',
          card: '#121927'
        },
        text: {
          DEFAULT: '#E6ECF1',
          muted: '#B7C2CC'
        },
        accent: {
          DEFAULT: '#7C6FF4',
          soft: '#A3BFFA'
        },
        border: 'rgba(163,191,250,0.12)'
      }
    }
  },
  plugins: [require('@tailwindcss/typography')]
}
```

### `postcss.config.cjs`
```js
module.exports = {
  plugins: {
    tailwindcss: {},
    autoprefixer: {}
  }
}
```

### `tsconfig.json`
```json
{
  "compilerOptions": {
    "strict": true,
    "baseUrl": ".",
    "paths": { "@/*": ["src/*"] }
  }
}
```

---

## 3) Base styles

### `src/styles/globals.css`
```css
@tailwind base;
@tailwind components;
@tailwind utilities;

:root {
  --ring: #A3BFFA;
}

html { scroll-behavior: smooth; }

.prose :where(code):not(:where(pre *)) {
  @apply px-1.5 py-0.5 rounded bg-bg-soft text-text;
}

.prose pre { @apply rounded-xl bg-bg-soft border border-border; }
```

---

## 4) Layouts & UI

### `src/layouts/Base.astro`
```astro
---
const { title = 'Autumn Nippert', description = 'CS • AI/ML • Music' } = Astro.props
---
<html lang="en" class="dark">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>{title}</title>
    <meta name="description" content={description} />
    <link rel="preconnect" href="https://rsms.me" />
    <link rel="stylesheet" href="/styles/globals.css" />
  </head>
  <body class="bg-bg text-text antialiased">
    <Header />
    <main class="mx-auto max-w-3xl px-4 py-12">
      <slot />
    </main>
    <Footer />
    <script>
      // Respect system preference on first paint
      const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches
      document.documentElement.classList.toggle('dark', prefersDark)
    </script>
  </body>
</html>
```

### `src/components/Header.astro`
```astro
---
const links = [
  { href: '/', label: 'Home' },
  { href: '/blog', label: 'Blog' }
]
---
<header class="sticky top-0 z-50 backdrop-blur supports-[backdrop-filter]:bg-bg/60 border-b border-border">
  <nav class="mx-auto max-w-3xl px-4 h-14 flex items-center justify-between">
    <a href="/" class="font-medium">Autumn</a>
    <ul class="flex gap-6 text-sm text-text-muted">
      {links.map(l => (<li><a class="hover:text-text" href={l.href}>{l.label}</a></li>))}
    </ul>
  </nav>
</header>
```

### `src/components/Footer.astro`
```astro
<footer class="mx-auto max-w-3xl px-4 py-10 text-sm text-text-muted border-t border-border">
  <div class="flex flex-wrap items-center justify-between gap-4">
    <span>© {new Date().getFullYear()} Autumn Nippert</span>
    <a href="/rss.xml" class="hover:text-text">RSS</a>
  </div>
</footer>
```

### `src/components/PostCard.astro`
```astro
---
const { href, title, summary, date } = Astro.props as {
  href: string; title: string; summary: string; date: string
}
---
<a href={href} class="block rounded-2xl border border-border bg-bg-card p-5 hover:border-white/20 transition">
  <h3 class="text-lg font-medium">{title}</h3>
  <p class="mt-2 text-sm text-text-muted">{summary}</p>
  <time class="mt-1 block text-xs text-text-muted">{new Date(date).toLocaleDateString()}</time>
</a>
```

### `src/components/Prose.astro`
```astro
---
---
<div class="prose prose-invert max-w-none prose-pre:shadow-md">
  <slot />
</div>
```

---

## 5) Content collections (blog)

### `src/content/config.ts`
```ts
import { defineCollection, z } from 'astro:content'

const blog = defineCollection({
  type: 'content',
  schema: z.object({
    title: z.string(),
    date: z.string(), // ISO
    summary: z.string(),
    tags: z.array(z.string()).optional(),
    draft: z.boolean().optional()
  })
})

export const collections = { blog }
```

### Example post: `src/content/blog/hello-world.mdx`
```mdx
---
title: Hello, Astro
date: 2025-08-08
summary: Spinning up a minimalist, dark-first Astro+MDX blog.
tags: [astro, mdx]
---

Welcome to the new blog. This supports **MDX**, so you can embed components inline.

```ts
export function add(a: number, b: number) { return a + b }
```
```

---

## 6) Pages

### `src/pages/index.astro`
```astro
---
import Base from '@/layouts/Base.astro'
---
<Base title="Autumn Nippert" description="CS • AI/ML • Music">
  <section class="space-y-6">
    <h1 class="text-3xl font-semibold tracking-tight">Autumn Nippert</h1>
    <p class="text-text-muted max-w-prose">Grad CS @ UNH • AI/ML • Parallel computing • Music. This is a refreshed site built with Astro + MDX.</p>
    <div class="mt-8">
      <a href="/blog" class="rounded-xl border border-border px-4 py-2 hover:border-white/20">Read the blog →</a>
    </div>
  </section>
</Base>
```

### `src/pages/blog/index.astro`
```astro
---
import Base from '@/layouts/Base.astro'
import PostCard from '@/components/PostCard.astro'
import { getCollection } from 'astro:content'
const posts = (await getCollection('blog'))
  .filter(p => !p.data.draft)
  .sort((a,b) => +new Date(b.data.date) - +new Date(a.data.date))
---
<Base title="Blog – Autumn">
  <h1 class="text-2xl font-semibold">Blog</h1>
  <div class="mt-8 grid gap-4">
    {posts.map(p => (
      <PostCard href={`/blog/${p.slug}`} title={p.data.title} summary={p.data.summary} date={p.data.date} />
    ))}
  </div>
</Base>
```

### `src/pages/blog/[slug].astro`
```astro
---
import Base from '@/layouts/Base.astro'
import Prose from '@/components/Prose.astro'
import { getCollection } from 'astro:content'

export async function getStaticPaths() {
  const posts = await getCollection('blog')
  return posts.map(p => ({ params: { slug: p.slug }, props: { post: p } }))
}
const { post } = Astro.props
const { Content } = await post.render()
---
<Base title={`${post.data.title} – Autumn`}>
  <article class="mt-4">
    <header class="mb-6">
      <h1 class="text-3xl font-semibold tracking-tight">{post.data.title}</h1>
      <time class="text-sm text-text-muted">{new Date(post.data.date).toLocaleDateString()}</time>
    </header>
    <Prose>
      <Content />
    </Prose>
  </article>
</Base>
```

### `src/pages/rss.xml.ts`
```ts
import rss from '@astrojs/rss'
import { getCollection } from 'astro:content'

export async function GET(context) {
  const posts = await getCollection('blog')
  return rss({
    title: 'Autumn – Blog',
    description: 'Notes on CS, AI/ML, and music',
    site: context.site ?? 'https://autumnnippert.com',
    items: posts
      .filter(p => !p.data.draft)
      .sort((a,b) => +new Date(b.data.date) - +new Date(a.data.date))
      .map(p => ({
        link: `/blog/${p.slug}`,
        title: p.data.title,
        pubDate: new Date(p.data.date),
        description: p.data.summary
      }))
  })
}
```

---

## 7) Run it
```bash
npm run dev
# open http://localhost:4321
```

---

## 8) Deploy
- **Vercel / Netlify:** zero-config for Astro. Set build command `astro build`, output `dist/`.
- **GitHub Pages:** `npm i -D gh-pages`, then `gh-pages -d dist`. Configure `site` in `astro.config.mjs`.

---

## 9) Next steps (optional)
- Add a `Projects` collection mirroring your existing portfolio.
- Add a `now` page, tags page, and simple search (page-filters by tag; later, client-side fuse.js).
- Add MDX shortcodes (Callout, Photo, LinkCard) for richer posts without heavy JS.
