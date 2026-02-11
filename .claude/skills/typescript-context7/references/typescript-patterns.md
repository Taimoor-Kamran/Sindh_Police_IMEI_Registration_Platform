# TypeScript Common Patterns

## Generic Patterns

### Generic Functions
```typescript
function identity<T>(arg: T): T {
    return arg;
}

function getProperty<T, K extends keyof T>(obj: T, key: K): T[K] {
    return obj[key];
}
```

### Generic Constraints
```typescript
interface Lengthwise {
    length: number;
}

function loggingIdentity<T extends Lengthwise>(arg: T): T {
    console.log(arg.length);
    return arg;
}
```

### Generic Classes
```typescript
class GenericNumber<T> {
    zeroValue: T;
    add: (x: T, y: T) => T;
}
```

## Type Guard Patterns

### typeof Guards
```typescript
function padLeft(value: string, padding: string | number) {
    if (typeof padding === "number") {
        return " ".repeat(padding) + value;
    }
    return padding + value;
}
```

### instanceof Guards
```typescript
function isDate(value: unknown): value is Date {
    return value instanceof Date;
}
```

### Custom Type Guards
```typescript
interface Fish { swim(): void; }
interface Bird { fly(): void; }

function isFish(pet: Fish | Bird): pet is Fish {
    return (pet as Fish).swim !== undefined;
}
```

### in Operator Guards
```typescript
function move(animal: Fish | Bird) {
    if ("swim" in animal) {
        return animal.swim();
    }
    return animal.fly();
}
```

## Mapped Types

### Basic Mapped Type
```typescript
type Readonly<T> = {
    readonly [P in keyof T]: T[P];
};

type Optional<T> = {
    [P in keyof T]?: T[P];
};
```

### Mapped Type with Remapping
```typescript
type Getters<T> = {
    [K in keyof T as `get${Capitalize<string & K>}`]: () => T[K];
};
```

## Conditional Types

### Basic Conditional
```typescript
type IsString<T> = T extends string ? true : false;
```

### Infer Keyword
```typescript
type ReturnType<T> = T extends (...args: any[]) => infer R ? R : never;

type UnwrapPromise<T> = T extends Promise<infer U> ? U : T;
```

### Distributive Conditionals
```typescript
type ToArray<T> = T extends any ? T[] : never;
// ToArray<string | number> = string[] | number[]
```

## Template Literal Types

### Basic Template Literals
```typescript
type EventName = `on${Capitalize<string>}`;

type Greeting = `Hello, ${string}!`;
```

### Template Literal with Union
```typescript
type Direction = "top" | "right" | "bottom" | "left";
type Margin = `margin-${Direction}`;
// "margin-top" | "margin-right" | "margin-bottom" | "margin-left"
```

## Discriminated Unions

### Tagged Union Pattern
```typescript
interface Square {
    kind: "square";
    size: number;
}

interface Rectangle {
    kind: "rectangle";
    width: number;
    height: number;
}

type Shape = Square | Rectangle;

function area(shape: Shape): number {
    switch (shape.kind) {
        case "square":
            return shape.size ** 2;
        case "rectangle":
            return shape.width * shape.height;
    }
}
```

## Module Patterns

### Barrel Exports
```typescript
// index.ts
export * from './user';
export * from './product';
export * from './order';
```

### Re-export with Rename
```typescript
export { User as UserModel } from './user';
export { default as api } from './api';
```

## Class Patterns

### Abstract Classes
```typescript
abstract class Animal {
    abstract makeSound(): void;

    move(): void {
        console.log("Moving...");
    }
}
```

### Mixins
```typescript
type Constructor<T = {}> = new (...args: any[]) => T;

function Timestamped<TBase extends Constructor>(Base: TBase) {
    return class extends Base {
        timestamp = Date.now();
    };
}
```

## Decorator Patterns

### Class Decorator
```typescript
function sealed(constructor: Function) {
    Object.seal(constructor);
    Object.seal(constructor.prototype);
}

@sealed
class Greeter {
    greeting: string;
    constructor(message: string) {
        this.greeting = message;
    }
}
```

### Method Decorator
```typescript
function log(target: any, key: string, descriptor: PropertyDescriptor) {
    const original = descriptor.value;
    descriptor.value = function(...args: any[]) {
        console.log(`Calling ${key} with`, args);
        return original.apply(this, args);
    };
    return descriptor;
}
```

## Error Handling Patterns

### Result Type
```typescript
type Result<T, E = Error> =
    | { success: true; value: T }
    | { success: false; error: E };

function parseJSON<T>(json: string): Result<T> {
    try {
        return { success: true, value: JSON.parse(json) };
    } catch (e) {
        return { success: false, error: e as Error };
    }
}
```

### Exhaustive Checking
```typescript
function assertNever(x: never): never {
    throw new Error("Unexpected object: " + x);
}

function handleShape(shape: Shape) {
    switch (shape.kind) {
        case "square": return shape.size ** 2;
        case "rectangle": return shape.width * shape.height;
        default: return assertNever(shape);
    }
}
```
