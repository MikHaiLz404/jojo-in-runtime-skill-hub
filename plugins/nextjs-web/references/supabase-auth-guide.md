# Supabase Auth Guide

## Setup with @supabase/ssr

### Middleware (middleware.ts)

```typescript
import { createServerClient } from '@supabase/ssr'
import { NextResponse } from 'next/server'

export async function middleware(request) {
  const response = NextResponse.next()
  const supabase = createServerClient(
    process.env.NEXT_PUBLIC_SUPABASE_URL,
    process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY,
    {
      cookies: {
        getAll() { return request.cookies.getAll() },
        setAll(cookiesToSet) {
          cookiesToSet.forEach(({ name, value, options }) =>
            response.cookies.set(name, value, options)
          )
        }
      }
    }
  )
  await supabase.auth.getUser()
  return response
}
```

### Client Auth Listener

```typescript
'use client'
import { useEffect } from 'react'
import { createBrowserClient } from '@supabase/ssr'

export default function AuthProvider({ children }) {
  const supabase = createBrowserClient(
    process.env.NEXT_PUBLIC_SUPABASE_URL,
    process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY
  )

  useEffect(() => {
    const { data: { subscription } } = supabase.auth.onAuthStateChange(())
    return () => subscription.unsubscribe()
  }, [supabase.auth])

  return <>{children}</>
}
```

## Protected Routes

Check session in Server Components:

```typescript
const { data: { user } } = await supabase.auth.getUser()
if (!user) redirect('/login')
```
