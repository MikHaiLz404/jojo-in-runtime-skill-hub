# App Router Patterns

## File-Based Routing

Next.js App Router uses file-system based routing in the `app/` directory.

### Route Segments

| File | Purpose |
|------|---------|
| `page.tsx` | UI for the route |
| `layout.tsx` | Shared layout |
| `loading.tsx` | Loading UI |
| `error.tsx` | Error UI |
| `not-found.tsx` | 404 UI |

### Dynamic Routes

```typescript
// app/blog/[slug]/page.tsx
export default function BlogPost({ params }: { params: { slug: string } }) {
  return <h1>Post: {params.slug}</h1>
}
```

## Parallel Routes

Use `@folder` convention for parallel routes.

## Intercepting Routes

Use `(.)folder` convention for intercepting routes.
