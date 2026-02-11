# Supabase Common Patterns

Quick reference for common Supabase patterns and best practices.

## Authentication

### Email/Password Sign Up

```typescript
const { data, error } = await supabase.auth.signUp({
  email: 'user@example.com',
  password: 'secure-password',
})
```

### Email/Password Sign In

```typescript
const { data, error } = await supabase.auth.signInWithPassword({
  email: 'user@example.com',
  password: 'secure-password',
})
```

### OAuth Sign In

```typescript
const { data, error } = await supabase.auth.signInWithOAuth({
  provider: 'google',
  options: {
    redirectTo: 'https://yourapp.com/auth/callback',
  },
})
```

### Magic Link

```typescript
const { data, error } = await supabase.auth.signInWithOtp({
  email: 'user@example.com',
  options: {
    emailRedirectTo: 'https://yourapp.com/welcome',
  },
})
```

### Sign Out

```typescript
const { error } = await supabase.auth.signOut()
```

### Get Current User

```typescript
const { data: { user } } = await supabase.auth.getUser()
```

### Auth State Change Listener

```typescript
supabase.auth.onAuthStateChange((event, session) => {
  console.log(event, session)
})
```

## Database Queries

### Select All

```typescript
const { data, error } = await supabase
  .from('posts')
  .select('*')
```

### Select with Columns

```typescript
const { data, error } = await supabase
  .from('posts')
  .select('id, title, content')
```

### Select with Related Data

```typescript
const { data, error } = await supabase
  .from('posts')
  .select(`
    id,
    title,
    author:profiles(name, avatar_url)
  `)
```

### Filter with Where

```typescript
const { data, error } = await supabase
  .from('posts')
  .select('*')
  .eq('status', 'published')
  .gte('created_at', '2024-01-01')
```

### Insert

```typescript
const { data, error } = await supabase
  .from('posts')
  .insert({ title: 'New Post', content: 'Hello World' })
  .select()
```

### Update

```typescript
const { data, error } = await supabase
  .from('posts')
  .update({ title: 'Updated Title' })
  .eq('id', 1)
  .select()
```

### Delete

```typescript
const { error } = await supabase
  .from('posts')
  .delete()
  .eq('id', 1)
```

### Upsert

```typescript
const { data, error } = await supabase
  .from('posts')
  .upsert({ id: 1, title: 'Updated or New' })
  .select()
```

## Row Level Security (RLS)

### Enable RLS

```sql
ALTER TABLE posts ENABLE ROW LEVEL SECURITY;
```

### Allow Read for All

```sql
CREATE POLICY "Allow public read" ON posts
FOR SELECT USING (true);
```

### Allow Insert for Authenticated Users

```sql
CREATE POLICY "Allow authenticated insert" ON posts
FOR INSERT TO authenticated
WITH CHECK (true);
```

### User Can Only See Own Data

```sql
CREATE POLICY "Users can view own posts" ON posts
FOR SELECT USING (auth.uid() = user_id);
```

### User Can Only Modify Own Data

```sql
CREATE POLICY "Users can update own posts" ON posts
FOR UPDATE USING (auth.uid() = user_id)
WITH CHECK (auth.uid() = user_id);
```

### Role-Based Access

```sql
CREATE POLICY "Admins can do everything" ON posts
FOR ALL USING (
  EXISTS (
    SELECT 1 FROM profiles
    WHERE id = auth.uid() AND role = 'admin'
  )
);
```

## Storage

### Upload File

```typescript
const { data, error } = await supabase.storage
  .from('avatars')
  .upload('user-avatar.png', file, {
    contentType: 'image/png',
    upsert: true,
  })
```

### Download File

```typescript
const { data, error } = await supabase.storage
  .from('avatars')
  .download('user-avatar.png')
```

### Get Public URL

```typescript
const { data } = supabase.storage
  .from('avatars')
  .getPublicUrl('user-avatar.png')
```

### Create Signed URL

```typescript
const { data, error } = await supabase.storage
  .from('private-files')
  .createSignedUrl('document.pdf', 3600) // 1 hour expiry
```

### Delete File

```typescript
const { error } = await supabase.storage
  .from('avatars')
  .remove(['user-avatar.png'])
```

### List Files

```typescript
const { data, error } = await supabase.storage
  .from('avatars')
  .list('folder', {
    limit: 100,
    offset: 0,
  })
```

## Edge Functions

### Create Function

```typescript
// supabase/functions/hello-world/index.ts
import { serve } from 'https://deno.land/std@0.168.0/http/server.ts'

serve(async (req) => {
  const { name } = await req.json()
  const data = {
    message: `Hello ${name}!`,
  }

  return new Response(JSON.stringify(data), {
    headers: { 'Content-Type': 'application/json' },
  })
})
```

### Invoke Function

```typescript
const { data, error } = await supabase.functions.invoke('hello-world', {
  body: { name: 'World' },
})
```

### Deploy Function

```bash
supabase functions deploy hello-world
```

## Realtime

### Subscribe to Changes

```typescript
const channel = supabase
  .channel('posts-changes')
  .on(
    'postgres_changes',
    { event: '*', schema: 'public', table: 'posts' },
    (payload) => {
      console.log('Change received!', payload)
    }
  )
  .subscribe()
```

### Subscribe to Specific Events

```typescript
const channel = supabase
  .channel('posts-inserts')
  .on(
    'postgres_changes',
    { event: 'INSERT', schema: 'public', table: 'posts' },
    (payload) => {
      console.log('New post!', payload.new)
    }
  )
  .subscribe()
```

### Broadcast Messages

```typescript
const channel = supabase.channel('room-1')

// Subscribe
channel.on('broadcast', { event: 'cursor' }, (payload) => {
  console.log('Cursor position:', payload)
})

// Send
channel.send({
  type: 'broadcast',
  event: 'cursor',
  payload: { x: 100, y: 200 },
})
```

### Presence

```typescript
const channel = supabase.channel('room-1')

channel.on('presence', { event: 'sync' }, () => {
  const state = channel.presenceState()
  console.log('Online users:', state)
})

channel.subscribe(async (status) => {
  if (status === 'SUBSCRIBED') {
    await channel.track({ user_id: 'user-1', online_at: new Date() })
  }
})
```

### Unsubscribe

```typescript
await supabase.removeChannel(channel)
```

## Database Functions

### Create Function

```sql
CREATE OR REPLACE FUNCTION get_user_posts(user_id uuid)
RETURNS SETOF posts AS $$
  SELECT * FROM posts WHERE posts.user_id = $1;
$$ LANGUAGE sql STABLE;
```

### Call Function

```typescript
const { data, error } = await supabase
  .rpc('get_user_posts', { user_id: 'uuid-here' })
```

## Client Setup

### JavaScript/TypeScript

```typescript
import { createClient } from '@supabase/supabase-js'

const supabase = createClient(
  'https://your-project.supabase.co',
  'your-anon-key'
)
```

### With Types

```typescript
import { createClient } from '@supabase/supabase-js'
import { Database } from './database.types'

const supabase = createClient<Database>(
  'https://your-project.supabase.co',
  'your-anon-key'
)
```

## Best Practices

1. **Always enable RLS** on tables with user data
2. **Use service role key** only on the server, never expose to client
3. **Validate inputs** before database operations
4. **Use transactions** for complex multi-step operations
5. **Index foreign keys** for better join performance
6. **Use realtime sparingly** - subscribe only to what you need
7. **Handle errors** consistently across your application
8. **Use TypeScript** with generated types for type safety
