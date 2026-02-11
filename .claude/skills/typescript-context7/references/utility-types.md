# TypeScript Utility Types Reference

## Object Type Utilities

### Partial<T>
Makes all properties optional.
```typescript
type Partial<T> = { [P in keyof T]?: T[P] };

interface User { name: string; age: number; }
type PartialUser = Partial<User>;
// { name?: string; age?: number; }
```

### Required<T>
Makes all properties required.
```typescript
type Required<T> = { [P in keyof T]-?: T[P] };

interface Props { name?: string; age?: number; }
type RequiredProps = Required<Props>;
// { name: string; age: number; }
```

### Readonly<T>
Makes all properties readonly.
```typescript
type Readonly<T> = { readonly [P in keyof T]: T[P] };

interface User { name: string; }
type ReadonlyUser = Readonly<User>;
// { readonly name: string; }
```

### Pick<T, K>
Picks specific properties from T.
```typescript
type Pick<T, K extends keyof T> = { [P in K]: T[P] };

interface User { name: string; age: number; email: string; }
type UserBasic = Pick<User, "name" | "email">;
// { name: string; email: string; }
```

### Omit<T, K>
Omits specific properties from T.
```typescript
type Omit<T, K extends keyof any> = Pick<T, Exclude<keyof T, K>>;

interface User { name: string; age: number; password: string; }
type SafeUser = Omit<User, "password">;
// { name: string; age: number; }
```

### Record<K, T>
Creates object type with keys K and values T.
```typescript
type Record<K extends keyof any, T> = { [P in K]: T };

type PageInfo = { title: string; };
type Page = "home" | "about" | "contact";
type Pages = Record<Page, PageInfo>;
// { home: PageInfo; about: PageInfo; contact: PageInfo; }
```

## Union Type Utilities

### Exclude<T, U>
Excludes types from T that are assignable to U.
```typescript
type Exclude<T, U> = T extends U ? never : T;

type T = Exclude<"a" | "b" | "c", "a">;
// "b" | "c"
```

### Extract<T, U>
Extracts types from T that are assignable to U.
```typescript
type Extract<T, U> = T extends U ? T : never;

type T = Extract<"a" | "b" | "c", "a" | "f">;
// "a"
```

### NonNullable<T>
Removes null and undefined from T.
```typescript
type NonNullable<T> = T extends null | undefined ? never : T;

type T = NonNullable<string | null | undefined>;
// string
```

## Function Type Utilities

### Parameters<T>
Extracts parameter types as tuple.
```typescript
type Parameters<T extends (...args: any) => any> =
    T extends (...args: infer P) => any ? P : never;

function greet(name: string, age: number): void {}
type GreetParams = Parameters<typeof greet>;
// [string, number]
```

### ReturnType<T>
Extracts return type of function.
```typescript
type ReturnType<T extends (...args: any) => any> =
    T extends (...args: any) => infer R ? R : any;

function getUser() { return { name: "John", age: 30 }; }
type User = ReturnType<typeof getUser>;
// { name: string; age: number; }
```

### ConstructorParameters<T>
Extracts constructor parameter types.
```typescript
type ConstructorParameters<T extends abstract new (...args: any) => any> =
    T extends abstract new (...args: infer P) => any ? P : never;

class User { constructor(public name: string, public age: number) {} }
type UserParams = ConstructorParameters<typeof User>;
// [string, number]
```

### InstanceType<T>
Extracts instance type of constructor.
```typescript
type InstanceType<T extends abstract new (...args: any) => any> =
    T extends abstract new (...args: any) => infer R ? R : any;

class User { name: string = ""; }
type UserInstance = InstanceType<typeof User>;
// User
```

### ThisParameterType<T>
Extracts the this parameter type.
```typescript
function toHex(this: Number) {
    return this.toString(16);
}
type T = ThisParameterType<typeof toHex>;
// Number
```

### OmitThisParameter<T>
Removes this parameter from function type.
```typescript
function toHex(this: Number) {
    return this.toString(16);
}
type T = OmitThisParameter<typeof toHex>;
// () => string
```

## String Type Utilities

### Uppercase<S>
Converts string literal to uppercase.
```typescript
type T = Uppercase<"hello">;
// "HELLO"
```

### Lowercase<S>
Converts string literal to lowercase.
```typescript
type T = Lowercase<"HELLO">;
// "hello"
```

### Capitalize<S>
Capitalizes first character.
```typescript
type T = Capitalize<"hello">;
// "Hello"
```

### Uncapitalize<S>
Lowercases first character.
```typescript
type T = Uncapitalize<"Hello">;
// "hello"
```

## Promise Utilities

### Awaited<T>
Unwraps Promise type recursively.
```typescript
type Awaited<T> = T extends Promise<infer U> ? Awaited<U> : T;

type T = Awaited<Promise<Promise<string>>>;
// string
```

## Combining Utility Types

### Common Patterns
```typescript
// Make specific fields optional
type PartialBy<T, K extends keyof T> = Omit<T, K> & Partial<Pick<T, K>>;

// Make specific fields required
type RequiredBy<T, K extends keyof T> = Omit<T, K> & Required<Pick<T, K>>;

// Deep partial
type DeepPartial<T> = {
    [P in keyof T]?: T[P] extends object ? DeepPartial<T[P]> : T[P];
};

// Deep readonly
type DeepReadonly<T> = {
    readonly [P in keyof T]: T[P] extends object ? DeepReadonly<T[P]> : T[P];
};

// Mutable (remove readonly)
type Mutable<T> = { -readonly [P in keyof T]: T[P] };

// Nullable
type Nullable<T> = { [P in keyof T]: T[P] | null };
```
