# Next Safe Action Common Patterns

Quick reference for common Next Safe Action patterns and best practices.

## Installation

```bash
npm install next-safe-action zod
```

## Action Client Setup

### Basic Setup

```typescript
// lib/safe-action.ts
import { createSafeActionClient } from "next-safe-action";

export const actionClient = createSafeActionClient();
```

### With Default Error Handler

```typescript
import { createSafeActionClient } from "next-safe-action";

export const actionClient = createSafeActionClient({
  handleReturnedServerError(e) {
    return "An error occurred";
  },
});
```

### With Middleware

```typescript
import { createSafeActionClient } from "next-safe-action";

export const actionClient = createSafeActionClient()
  .use(async ({ next }) => {
    // Middleware logic here
    return next({ ctx: { userId: "123" } });
  });
```

## Basic Server Actions

### Simple Action with Validation

```typescript
"use server";

import { z } from "zod";
import { actionClient } from "@/lib/safe-action";

const inputSchema = z.object({
  username: z.string().min(3).max(10),
  password: z.string().min(8).max(100),
});

export const loginUser = actionClient
  .inputSchema(inputSchema)
  .action(async ({ parsedInput: { username, password } }) => {
    // Server-side logic here
    return { success: true };
  });
```

### Action with Metadata

```typescript
"use server";

import { z } from "zod";
import { actionClient } from "@/lib/safe-action";

const inputSchema = z.object({
  id: z.string().uuid(),
  body: z.string().min(1),
});

export const createTodo = actionClient
  .metadata({ actionName: "createTodo" })
  .inputSchema(inputSchema)
  .action(async ({ parsedInput }) => {
    // Create todo logic
    return { createdTodo: parsedInput };
  });
```

### Action with Context from Middleware

```typescript
"use server";

import { z } from "zod";
import { authClient } from "@/lib/safe-action";

const inputSchema = z.object({
  title: z.string().min(1),
});

export const createPost = authClient
  .inputSchema(inputSchema)
  .action(async ({ parsedInput, ctx }) => {
    // ctx.userId available from middleware
    return { post: { ...parsedInput, userId: ctx.userId } };
  });
```

## Client-Side Hooks

### useAction Hook

```typescript
"use client";

import { useAction } from "next-safe-action/hooks";
import { loginUser } from "./actions";

export function LoginForm() {
  const { execute, result, status, isExecuting } = useAction(loginUser);

  return (
    <form
      onSubmit={(e) => {
        e.preventDefault();
        execute({ username: "john", password: "password123" });
      }}
    >
      {status === "executing" && <p>Logging in...</p>}
      {result.data?.success && <p>Login successful!</p>}
      {result.validationErrors && <p>Validation failed</p>}
      <button type="submit" disabled={isExecuting}>
        Login
      </button>
    </form>
  );
}
```

### useAction with Callbacks

```typescript
"use client";

import { useAction } from "next-safe-action/hooks";
import { createPost } from "./actions";

export function PostForm() {
  const { execute, isExecuting } = useAction(createPost, {
    onSuccess: ({ data }) => {
      console.log("Post created:", data);
    },
    onError: ({ error }) => {
      console.error("Error:", error);
    },
    onSettled: () => {
      console.log("Action completed");
    },
  });

  return (
    <button onClick={() => execute({ title: "New Post" })}>
      Create Post
    </button>
  );
}
```

### useOptimisticAction Hook

```typescript
"use client";

import { useOptimisticAction } from "next-safe-action/hooks";
import { addTodo } from "./actions";

export function TodoList({ todos }: { todos: Todo[] }) {
  const { execute, optimisticState } = useOptimisticAction(addTodo, {
    currentState: todos,
    updateFn: (state, input) => {
      return [...state, { ...input, pending: true }];
    },
  });

  return (
    <ul>
      {optimisticState.map((todo) => (
        <li key={todo.id} style={{ opacity: todo.pending ? 0.5 : 1 }}>
          {todo.body}
        </li>
      ))}
    </ul>
  );
}
```

## Error Handling

### Returning Validation Errors

```typescript
"use server";

import { z } from "zod";
import { returnValidationErrors } from "next-safe-action";
import { actionClient } from "@/lib/safe-action";

const inputSchema = z.object({
  email: z.string().email(),
});

export const registerUser = actionClient
  .inputSchema(inputSchema)
  .action(async ({ parsedInput: { email } }) => {
    const existingUser = await db.user.findByEmail(email);

    if (existingUser) {
      return returnValidationErrors(inputSchema, {
        email: {
          _errors: ["Email already registered"],
        },
      });
    }

    // Continue with registration...
    return { success: true };
  });
```

### Root-Level Validation Errors

```typescript
return returnValidationErrors(inputSchema, {
  _errors: ["Invalid credentials"],
});
```

### Server Error Handling

```typescript
"use server";

import { actionClient } from "@/lib/safe-action";

export const riskyAction = actionClient
  .action(async () => {
    try {
      // Risky operation
    } catch (error) {
      throw new Error("Something went wrong");
    }
  });
```

## Middleware Patterns

### Authentication Middleware

```typescript
import { createSafeActionClient } from "next-safe-action";
import { getSession } from "@/lib/auth";

export const authClient = createSafeActionClient()
  .use(async ({ next }) => {
    const session = await getSession();

    if (!session) {
      throw new Error("Unauthorized");
    }

    return next({ ctx: { userId: session.userId } });
  });
```

### Chained Middleware

```typescript
export const adminClient = authClient
  .use(async ({ next, ctx }) => {
    const user = await db.user.findById(ctx.userId);

    if (user?.role !== "admin") {
      throw new Error("Forbidden");
    }

    return next({ ctx: { ...ctx, isAdmin: true } });
  });
```

## Bind Arguments

### Binding Arguments to Actions

```typescript
"use server";

import { z } from "zod";
import { actionClient } from "@/lib/safe-action";

const inputSchema = z.object({
  content: z.string().min(1),
});

export const updatePost = actionClient
  .bindArgsSchemas([z.string().uuid()]) // postId
  .inputSchema(inputSchema)
  .action(async ({ parsedInput, bindArgsParsedInputs: [postId] }) => {
    // Update post with postId
    return { updated: true };
  });
```

### Using Bound Actions in Client

```typescript
"use client";

import { useAction } from "next-safe-action/hooks";
import { updatePost } from "./actions";

export function EditPost({ postId }: { postId: string }) {
  const boundAction = updatePost.bind(null, postId);
  const { execute } = useAction(boundAction);

  return (
    <button onClick={() => execute({ content: "Updated content" })}>
      Update
    </button>
  );
}
```

## Direct Execution

### Without Hooks

```typescript
"use client";

import { loginUser } from "./actions";

export function LoginButton() {
  const handleLogin = async () => {
    const result = await loginUser({
      username: "john",
      password: "password123",
    });

    if (result.data?.success) {
      console.log("Logged in!");
    }

    if (result.validationErrors) {
      console.log("Validation failed:", result.validationErrors);
    }

    if (result.serverError) {
      console.log("Server error:", result.serverError);
    }
  };

  return <button onClick={handleLogin}>Login</button>;
}
```

## Best Practices

1. **Always use "use server"** directive at the top of action files
2. **Define input schemas** for all actions to ensure type safety
3. **Use middleware** for authentication and authorization
4. **Handle errors gracefully** with returnValidationErrors
5. **Use metadata** for action identification and logging
6. **Prefer hooks** (useAction, useOptimisticAction) for reactive UI
7. **Bind arguments** for reusable actions with partial parameters
8. **Revalidate paths** after mutations with Next.js revalidatePath
