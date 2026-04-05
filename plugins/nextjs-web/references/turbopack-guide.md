# Turbopack Guide

## Overview

Turbopack is the default bundler for Next.js 16+ development. It's written in Rust and provides:
- 5-14x faster cold starts
- Faster HMR (Hot Module Replacement)
- File-system caching

## Commands

```bash
# Default - Turbopack enabled
next dev

# Disable Turbopack (use webpack)
next dev --webpack

# Production build
next build

# Start production server
next start
```

## Cache

Turbopack uses file-system caching under `.next/`. Restarts reuse previous work.

## Troubleshooting

If dev is slow:
1. Ensure Turbopack is enabled (default)
2. Check `.next/` cache isn't corrupted
3. Consider `rm -rf .next` if cache is problematic
