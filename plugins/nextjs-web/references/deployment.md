# Deployment Guide

## Vercel Deployment

### Automatic Deployments

1. Push to GitHub
2. Vercel auto-detects Next.js
3. Preview deployments for PRs
4. Production deployment on merge to main

### Environment Variables

Set in Vercel dashboard:
- `NEXT_PUBLIC_SUPABASE_URL`
- `NEXT_PUBLIC_SUPABASE_ANON_KEY`
- Other env vars

### Build Settings

Vercel automatically uses:
- `next build` for production
- Turbopack for dev (local only)

## Performance Checklist

- [ ] TypeScript compiles without errors
- [ ] All tests passing
- [ ] Linting clean
- [ ] LCP < 2.5s
- [ ] CLS < 0.1
- [ ] FID < 100ms
- [ ] Accessibility (WCAG 2.1)
- [ ] Responsive design verified
