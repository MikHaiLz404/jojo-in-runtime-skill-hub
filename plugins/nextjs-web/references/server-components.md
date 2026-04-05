# Server Components

## When to Use Server vs Client Components

### Server Components (default)
- Fetch data
- Access backend resources
- Keep sensitive info on server
- Reduce client-side JS

### Client Components (`'use client'`)
- Add interactivity
- Use browser APIs
- Use state/useEffect
- Event listeners

## Data Fetching

```typescript
// Server Component - direct DB access
async function Posts() {
  const posts = await db.post.findMany()
  return <ul>{posts.map(p => <li key={p.id}>{p.title}</li>)}</ul>
}
```

## Caching

Use `fetch()` with cache options or React Cache for data caching.
