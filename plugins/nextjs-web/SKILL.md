---
name: nextjs-web
description: "Complete Next.js web development: React 18+, App Router, Server Components, TypeScript, Tailwind CSS, Supabase Auth, and Turbopack optimization. Use when: building Next.js apps, React components, authentication, performance optimization."
risk: safe
source: "combined (nextjs-supabase-auth, nextjs-turbopack, react-nextjs-development)"
date_added: "2026-04-05"
---

# Next.js Web Development

Comprehensive Next.js 14+ development with React 18+, App Router, Server Components, TypeScript, Tailwind CSS, Supabase Auth integration, and Turbopack performance optimization.

## Core Technologies

| Category | Technology |
|----------|------------|
| Framework | Next.js 14+, React 18+ |
| Language | TypeScript 5+ |
| Bundler | Turbopack (default dev) |
| Styling | Tailwind CSS v4 |
| Auth | Supabase Auth (@supabase/ssr) |
| Deployment | Vercel |

## When to Use

- Building new React/Next.js applications
- Creating Next.js 14+ projects with App Router
- Implementing Server Components
- Setting up TypeScript with React
- Styling with Tailwind CSS
- Building full-stack Next.js applications
- Adding Supabase authentication
- Optimizing dev speed with Turbopack

---

# Part 1: Turbopack & Dev Speed

Next.js 16+ uses Turbopack by default for local development: an incremental bundler written in Rust that significantly speeds up dev startup and hot updates.

## Turbopack Commands

```bash
next dev          # Development with Turbopack (default)
next build        # Production build
next start        # Start production server
```

## Turbopack Guidelines

- **Turbopack (default dev)**: Use for day-to-day development. Faster cold start and HMR, especially in large apps.
- **Webpack (legacy dev)**: Use only if you hit a Turbopack bug or rely on a webpack-only plugin. Disable with `--webpack`.
- **Bundle Analyzer (Next.js 16.1+)**: Enable via config for inspecting output and finding heavy dependencies.

## Best Practices

- Stay on a recent Next.js 16.x for stable Turbopack and caching behavior
- If dev is slow, ensure you're on Turbopack (default) and cache isn't being cleared
- For production bundle size issues, use official Next.js bundle analysis tooling

---

# Part 2: Supabase Auth Integration

Expert integration of Supabase Auth with Next.js App Router using @supabase/ssr.

## Core Principles

1. Use @supabase/ssr for App Router integration
2. Handle tokens in middleware for protected routes
3. Never expose auth tokens to client unnecessarily
4. Use Server Actions for auth operations when possible
5. Understand the cookie-based session flow

## Security Considerations

- Always validate session on server side
- Use httpOnly cookies for auth tokens
- Avoid exposing access tokens to client
- Protect all sensitive routes via middleware
- Validate OAuth callback origin

## Auth Patterns

### Supabase Client Setup

Create properly configured Supabase clients for different contexts (server, client, middleware).

### Auth Middleware

Protect routes and refresh sessions in middleware.

### Auth Callback Route

Handle OAuth callback and exchange code for session.

## Anti-Patterns

- **getSession in Server Components** - Don't use this pattern
- **Auth State in Client Without Listener** - Always set up auth state listener
- **Storing Tokens Manually** - Use @supabase/ssr instead

---

# Part 3: React/Next.js Development Workflow

## Phase 1: Project Setup

### Actions
1. Choose project type (React SPA, Next.js app)
2. Select build tool (Next.js with Turbopack)
3. Scaffold project structure
4. Configure TypeScript
5. Set up ESLint and Prettier

## Phase 2: Component Architecture

### Actions
1. Design component hierarchy
2. Create base components
3. Implement layout components
4. Set up state management (Zustand, React Query)
5. Create custom hooks

## Phase 3: Styling and Design

### Actions
1. Set up Tailwind CSS v4
2. Configure design tokens
3. Create utility classes
4. Build component styles
5. Implement responsive design

## Phase 4: Data Fetching

### Actions
1. Implement Server Components
2. Set up React Query/SWR
3. Create API client
4. Handle loading states
5. Implement error boundaries

## Phase 5: Routing and Navigation

### Actions
1. Set up file-based routing (App Router)
2. Create dynamic routes
3. Implement nested routes
4. Add route guards
5. Configure redirects

## Phase 6: Forms and Validation

### Actions
1. Choose form library (React Hook Form, Formik)
2. Set up validation (Zod, Yup)
3. Create form components
4. Handle submissions
5. Implement error handling

## Phase 7: Testing

### Actions
1. Set up testing framework (Vitest)
2. Write unit tests
3. Create component tests
4. Implement E2E tests (Playwright)
5. Configure CI integration

## Phase 8: Build and Deployment

### Actions
1. Configure build settings
2. Optimize bundle size
3. Set up environment variables
4. Deploy to Vercel
5. Configure preview deployments

## Quality Gates

- TypeScript compiles without errors
- All tests passing
- Linting clean
- Performance metrics met (LCP, CLS, FID)
- Accessibility checked (WCAG 2.1)
- Responsive design verified

## Safety Notes

- Validate all user inputs in forms
- Sanitize API responses before rendering
- Avoid exposing sensitive data in client components
