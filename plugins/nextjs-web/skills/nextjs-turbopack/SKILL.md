---
name: nextjs-turbopack
description: "Next.js 16+ and Turbopack — incremental bundling, FS caching, dev speed, and when to use Turbopack vs webpack."
risk: safe
origin: "ECC"
date_added: "2026-04-05"
---

# Next.js and Turbopack

Next.js 16+ uses Turbopack by default for local development: an incremental bundler written in Rust that significantly speeds up dev startup and hot updates.

## When to Use

- **Turbopack (default dev)**: Use for day-to-day development. Faster cold start and HMR, especially in large apps.
- **Webpack (legacy dev)**: Use only if you hit a Turbopack bug or rely on a webpack-only plugin. Disable with `--webpack`.
- **Production**: Production build may use Turbopack or webpack depending on Next.js version.

Use when: developing or debugging Next.js 16+ apps, diagnosing slow dev startup or HMR, or optimizing production bundles.

## How It Works

- **Turbopack**: Incremental bundler for Next.js dev. Uses file-system caching so restarts are much faster (e.g. 5–14x on large projects).
- **Default in dev**: From Next.js 16, `next dev` runs with Turbopack unless disabled.
- **File-system caching**: Restarts reuse previous work; cache is typically under `.next`.

## Commands

```bash
next dev          # Development with Turbopack (default)
next build        # Production build
next start        # Start production server
```

## Best Practices

- Stay on a recent Next.js 16.x for stable Turbopack and caching behavior
- If dev is slow, ensure you're on Turbopack (default) and cache isn't being cleared
- For production bundle size issues, use official Next.js bundle analysis tooling
